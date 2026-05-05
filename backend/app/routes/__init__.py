from flask import Blueprint, jsonify, request, send_from_directory, current_app, g, send_file
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from functools import wraps
import bcrypt
import jwt
import datetime
import io
import os
import logging
import re
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from groq import Groq
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.database import db
from app.models import Carti, Users, CartiCitite, Recenzii, Anunturi, AnunturiAprecieri, CereriCarti

main_bp = Blueprint('main', __name__, url_prefix='/api')

ALLOWED_EXTENSIONS = frozenset({'png', 'jpg', 'jpeg', 'gif', 'webp'})
ALLOWED_EMAIL_DOMAIN = 'cni-sv.ro'
VALID_ROLES = frozenset({'user', 'bibliotecar'})
ALLOWED_BOOK_FIELDS = frozenset({'titlu', 'autor', 'ISBN', 'stoc_total', 'stoc_disponibil', 'gen', 'pozitie'})
ALLOWED_ANUNT_FIELDS = frozenset({'titlu', 'anunt'})

logger = logging.getLogger(__name__)
ROLE_ALIASES = {
    '1': 'bibliotecar',
    'administrator': 'bibliotecar',
    'admin': 'bibliotecar',
    'bibliotecar': 'bibliotecar',
    'user': 'user'
}
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9._%+\-]{0,62}[A-Za-z0-9])?@([A-Za-z0-9\-]+\.)+[A-Za-z]{2,63}$")
PROFILE_PICTURES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'profile_pictures')
BOOK_IMAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'book_images')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def _find_files_by_prefix(directory, prefix):
    """Caută fișiere în director cu prefixul dat și extensie permisă.
    Folosește os.listdir în loc de glob ca să evite glob injection din
    șiruri controlate de utilizator care conțin *, ?, sau [].
    """
    os.makedirs(directory, exist_ok=True)
    rezultate = []
    for fisier in os.listdir(directory):
        if not fisier.startswith(prefix + '.'):
            continue
        ext = fisier.rsplit('.', 1)[1].lower() if '.' in fisier else ''
        if ext in ALLOWED_EXTENSIONS:
            rezultate.append(fisier)
    return rezultate


# ── Helper email ─────────────────────────────────────────────

def send_email(recipients, subject, html_body):
    """Trimite un email prin SMTP (Gmail).

    Citește setările SMTP_* din config-ul Flask.
    Returnează True la succes, False la eroare (logat, nu aruncă excepție).
    """
    cfg = current_app.config
    host = cfg.get('SMTP_HOST', 'smtp.gmail.com')
    port = cfg.get('SMTP_PORT', 587)
    user = cfg.get('SMTP_USER', '')
    password = cfg.get('SMTP_PASSWORD', '')
    sender = cfg.get('SMTP_FROM', '') or user

    if not user or not password:
        logger.error('Credențiale SMTP lipsă — emailul nu a fost trimis')
        return False

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    msg.attach(MIMEText(html_body, 'html'))

    try:
        with smtplib.SMTP(host, port, timeout=10) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(user, password)
            server.sendmail(sender, recipients, msg.as_string())
        logger.info('Email trimis către %s', recipients)
        return True
    except Exception:
        logger.exception('Eroare la trimiterea emailului')
        return False


# ── Helpers JWT ──────────────────────────────────────────────

def normalize_role(raw_role):
    """Normalizează valorile vechi de rol la setul suportat."""
    if raw_role is None:
        return 'user'

    rol_normalizat = ROLE_ALIASES.get(str(raw_role).strip().lower())
    return rol_normalizat if rol_normalizat in VALID_ROLES else 'user'


def normalize_cni_email(email):
    """Returnează adresa de email școlară normalizată sau None dacă e invalidă."""
    if not isinstance(email, str):
        return None

    email_normalizat = email.strip().lower()
    if not email_normalizat or len(email_normalizat) > 254:
        return None

    if not EMAIL_REGEX.fullmatch(email_normalizat):
        return None

    parte_locala, _, domeniu = email_normalizat.rpartition('@')
    if not parte_locala or '..' in parte_locala or domeniu != ALLOWED_EMAIL_DOMAIN:
        return None

    return email_normalizat


def fetch_user_by_id(user_id):
    """Încarcă utilizatorul curent din baza de date pentru verificări de autorizare."""
    query = text(
        "SELECT user_id, username, email, rol FROM users WHERE user_id = :user_id"
    )
    result = db.session.execute(query, {'user_id': user_id}).mappings().first()
    if not result:
        return None

    return {
        'user_id': result['user_id'],
        'username': result['username'],
        'email': result['email'],
        'rol': normalize_role(result['rol'])
    }


def create_jwt_token(user_id, username, email):
    """Creează un token JWT cu date de identitate."""
    payload = {
        'user_id': user_id,
        'username': username,
        'email': email,
        'iat': datetime.datetime.now(datetime.timezone.utc),
        'exp': datetime.datetime.now(datetime.timezone.utc) + current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')


def set_jwt_cookie(response, token):
    """Setează tokenul JWT ca cookie httpOnly pe răspuns."""
    response.set_cookie(
        current_app.config['JWT_COOKIE_NAME'],
        token,
        httponly=True,
        secure=current_app.config['JWT_COOKIE_SECURE'],
        samesite=current_app.config['JWT_COOKIE_SAMESITE'],
        max_age=int(current_app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds()),
        path='/'
    )
    return response


def clear_jwt_cookie(response):
    """Șterge cookie-ul JWT."""
    response.set_cookie(
        current_app.config['JWT_COOKIE_NAME'],
        '',
        httponly=True,
        secure=current_app.config['JWT_COOKIE_SECURE'],
        samesite=current_app.config['JWT_COOKIE_SAMESITE'],
        max_age=0,
        path='/'
    )
    return response


def decode_jwt_token(token):
    """Decodează și verifică un token JWT. Returnează payload sau None."""
    try:
        return jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def get_current_user():
    """Rezolvă utilizatorul autentificat din cookie-ul JWT și baza de date.
    Cachează rezultatul pe flask.g ca să nu se mai facă query la DB
    pentru apeluri repetate în aceeași cerere.
    """
    if hasattr(g, '_current_user'):
        return g._current_user

    token = request.cookies.get(current_app.config['JWT_COOKIE_NAME'])
    if not token:
        g._current_user = None
        return None

    payload = decode_jwt_token(token)
    if not payload:
        g._current_user = None
        return None

    try:
        user_id = int(payload.get('user_id'))
    except (TypeError, ValueError):
        g._current_user = None
        return None

    g._current_user = fetch_user_by_id(user_id)
    return g._current_user


def jwt_required(f):
    """Decorator care impune prezența unui cookie JWT valid."""
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({'success': False, 'message': 'Autentificare necesară'}), 401
        request.current_user = user
        return f(*args, **kwargs)
    return decorated


def role_required(role):
    """Fabrică de decorator care impune un anumit rol verificat din baza de date."""
    if role not in VALID_ROLES:
        raise ValueError(f"Rol necunoscut: {role}")

    def decorator(f):
        @wraps(f)
        @jwt_required
        def decorated(*args, **kwargs):
            if request.current_user.get('rol') != role:
                return jsonify({'success': False, 'message': f'Necesită rol de {role}'}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator


bibliotecar_required = role_required('bibliotecar')

@main_bp.route('/health', methods=['GET'])
def health_check():
    """Endpoint de verificare a stării serverului."""
    return jsonify({'status': 'ok', 'message': 'Server is running'}), 200

@main_bp.route('/', methods=['GET'])
def index():
    """Index API — verifică conexiunea la baza de date."""
    return jsonify({
        'name': 'School Library API',
        'version': '1.0.0',
        'message': 'Database connection established'
    }), 200

@main_bp.route('/books', methods=['GET'])
def get_books():
    """Returnează toate cărțile din catalogul bibliotecii."""
    try:
        result = db.session.execute(text('SELECT carte_id, titlu, autor, ISBN, stoc_total, stoc_disponibil, imprumutat, gen, pozitie FROM carti'))
        books = []
        for row in result:
            books.append({
                'carte_id': row[0],
                'titlu': row[1],
                'autor': row[2],
                'ISBN': row[3],
                'stoc_total': row[4],
                'stoc_disponibil': row[5],
                'imprumutat': row[6],
                'gen': row[7],
                'pozitie': row[8]
            })
        return jsonify({'books': books}), 200
    except Exception:
        logger.exception('Eroare la preluarea cărților')
        return jsonify({'error': 'Eroare la preluarea cărților'}), 500


@main_bp.route('/books', methods=['POST'])
@bibliotecar_required
def add_book():
    """Adaugă o carte nouă în colecție. Necesită rol de bibliotecar."""
    data = request.get_json(silent=True) or {}
    titlu = data.get('titlu')
    autor = data.get('autor')
    isbn = data.get('ISBN')
    stoc_total = data.get('stoc_total', 1)
    stoc_disponibil = data.get('stoc_disponibil', stoc_total)
    gen = data.get('gen')
    pozitie = data.get('pozitie') or None

    if not titlu or not autor or not isbn or not gen:
        return jsonify({'success': False, 'message': 'titlu, autor, ISBN și gen sunt obligatorii'}), 400

    insert_query = text(
        "INSERT INTO carti (titlu, autor, ISBN, stoc_total, stoc_disponibil, imprumutat, gen, pozitie) "
        "VALUES (:titlu, :autor, :ISBN, :stoc_total, :stoc_disponibil, :imprumutat, :gen, :pozitie)"
    )
    try:
        db.session.execute(insert_query, {
            'titlu': titlu,
            'autor': autor,
            'ISBN': isbn,
            'stoc_total': stoc_total,
            'stoc_disponibil': stoc_disponibil,
            'imprumutat': stoc_disponibil < stoc_total,
            'gen': gen,
            'pozitie': pozitie
        })
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Există deja o carte cu acest ISBN'}), 409
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Eroare la adăugarea cărții'}), 500

    return jsonify({'success': True, 'message': 'Carte adăugată cu succes'}), 201


@main_bp.route('/books/<int:carte_id>', methods=['PUT'])
@bibliotecar_required
def update_book(carte_id):
    """Actualizează stocul sau detaliile unei cărți. Necesită rol de bibliotecar."""
    data = request.get_json(silent=True) or {}

    # Construiește query-ul dinamic de update
    fields = {}
    for key in ALLOWED_BOOK_FIELDS:
        if key in data:
            fields[key] = data[key]

    if not fields:
        return jsonify({'success': False, 'message': 'Niciun câmp de actualizat'}), 400

    set_clause = ', '.join(f"{k} = :{k}" for k in fields)
    fields['carte_id'] = carte_id

    # Actualizează automat flag-ul imprumutat dacă se schimbă stocul
    if 'stoc_total' in fields or 'stoc_disponibil' in fields:
        set_clause += ', imprumutat = (stoc_disponibil < stoc_total)'

    update_query = text(f"UPDATE carti SET {set_clause} WHERE carte_id = :carte_id")
    try:
        result = db.session.execute(update_query, fields)
        db.session.commit()
        if result.rowcount == 0:
            return jsonify({'success': False, 'message': 'Cartea nu a fost găsită'}), 404
    except IntegrityError:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Conflict ISBN'}), 409
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Eroare la actualizarea cărții'}), 500

    return jsonify({'success': True, 'message': 'Carte actualizată cu succes'}), 200


@main_bp.route('/books/<int:carte_id>', methods=['DELETE'])
@bibliotecar_required
def delete_book(carte_id):
    """Șterge o carte și toate înregistrările asociate. Necesită rol de bibliotecar."""
    try:
        db.session.execute(text("DELETE FROM imprumuturi_active WHERE carte_id = :id"), {'id': carte_id})
        db.session.execute(text("DELETE FROM cereri_carti WHERE carte_id = :id"), {'id': carte_id})
        db.session.execute(text("DELETE FROM recenzii WHERE carte_id = :id"), {'id': carte_id})
        db.session.execute(text("DELETE FROM carti_citite WHERE carte_id = :id"), {'id': carte_id})
        result = db.session.execute(text("DELETE FROM carti WHERE carte_id = :id"), {'id': carte_id})
        db.session.commit()
        if result.rowcount == 0:
            return jsonify({'success': False, 'message': 'Cartea nu a fost găsită'}), 404
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Eroare la ștergerea cărții'}), 500

    return jsonify({'success': True, 'message': 'Carte ștearsă cu succes'}), 200


@main_bp.route('/books/<int:carte_id>/request-fizic', methods=['POST'])
@jwt_required
def request_book_fizic(carte_id):
    """Trimite o cerere de împrumut fizic pentru o carte.

    Notifică prin email toți utilizatorii cu rolul 'bibliotecar'
    că elevul dorește să ridice cartea.
    """
    user = request.current_user

    # Căutăm cartea în baza de date
    book_row = db.session.execute(
        text("SELECT titlu, autor, stoc_disponibil FROM carti WHERE carte_id = :id"),
        {'id': carte_id}
    ).fetchone()

    if not book_row:
        return jsonify({'success': False, 'message': 'Cartea nu a fost găsită'}), 404

    titlu, autor, stoc_disponibil = book_row
    if stoc_disponibil <= 0:
        return jsonify({'success': False, 'message': 'Cartea nu este disponibilă'}), 409

    # Preluăm emailurile tuturor bibliotecarilor
    rows = db.session.execute(
        text("SELECT email FROM users WHERE rol = 'bibliotecar'")
    ).fetchall()
    emailuri_bibliotecari = [r[0] for r in rows if r[0]]

    if not emailuri_bibliotecari:
        logger.warning('Niciun bibliotecar găsit pentru notificarea cererii %d', carte_id)
        return jsonify({'success': False, 'message': 'Niciun bibliotecar disponibil să proceseze cererea'}), 503

    subject = f'Cerere împrumut carte — {titlu}'
    html_body = (
        f'<h2>Cerere nouă de împrumut</h2>'
        f'<p>Utilizatorul <strong>{user["username"]}</strong> '
        f'(<a href="mailto:{user["email"]}">{user["email"]}</a>) '
        f'dorește să împrumute cartea:</p>'
        f'<ul>'
        f'<li><strong>Titlu:</strong> {titlu}</li>'
        f'<li><strong>Autor:</strong> {autor}</li>'
        f'<li><strong>ID carte:</strong> {carte_id}</li>'
        f'</ul>'
        f'<p>Stoc disponibil: {stoc_disponibil}</p>'
    )

    # Salvăm cererea în baza de date
    try:
        db.session.execute(
            text("INSERT INTO cereri_carti (user_id, carte_id) VALUES (:uid, :cid)"),
            {'uid': user['user_id'], 'cid': carte_id}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        logger.exception('Eroare la salvarea cererii în DB')
        return jsonify({'success': False, 'message': 'Eroare la salvarea cererii'}), 500

    # Trimitem emailul (best-effort — cererea nu eșuează dacă emailul nu merge)
    send_email(emailuri_bibliotecari, subject, html_body)

    return jsonify({'success': True, 'message': 'Cererea a fost trimisă!'}), 200


@main_bp.route('/book-requests', methods=['GET'])
@bibliotecar_required
def get_book_requests():
    """Listează toate cererile de împrumut. Doar bibliotecar."""
    status_filter = request.args.get('status')  # opțional: pending, approved, rejected
    try:
        sql = (
            "SELECT c.cerere_id, c.user_id, c.carte_id, c.status, c.created_at, "
            "u.username, u.email, ca.titlu, ca.autor "
            "FROM cereri_carti c "
            "JOIN users u ON c.user_id = u.user_id "
            "JOIN carti ca ON c.carte_id = ca.carte_id "
        )
        params = {}
        if status_filter in ('pending', 'approved', 'rejected'):
            sql += "WHERE c.status = :status "
            params['status'] = status_filter
        sql += "ORDER BY c.created_at DESC"

        rows = db.session.execute(text(sql), params).fetchall()
        cereri = []
        for r in rows:
            cereri.append({
                'cerere_id': r[0],
                'user_id': r[1],
                'carte_id': r[2],
                'status': r[3],
                'created_at': r[4].isoformat() if r[4] else None,
                'username': r[5],
                'email': r[6],
                'titlu': r[7],
                'autor': r[8]
            })
        return jsonify({'success': True, 'cereri': cereri}), 200
    except Exception:
        logger.exception('Eroare la preluarea cererilor de împrumut')
        return jsonify({'success': False, 'error': 'Eroare la preluarea cererilor'}), 500


@main_bp.route('/book-requests/<int:cerere_id>', methods=['PUT'])
@bibliotecar_required
def update_book_request(cerere_id):
    """Aprobă sau respinge o cerere de împrumut. Doar bibliotecar."""
    data = request.get_json(silent=True) or {}
    status_nou = data.get('status')
    if status_nou not in ('approved', 'rejected'):
        return jsonify({'success': False, 'message': 'Status trebuie să fie approved sau rejected'}), 400

    # Intervalul de ridicare (obligatoriu doar la aprobare)
    pickup_from_str = (data.get('pickup_from') or '').strip()
    pickup_until_str = (data.get('pickup_until') or '').strip()
    if status_nou == 'approved' and (not pickup_from_str or not pickup_until_str):
        return jsonify({'success': False, 'message': 'pickup_from și pickup_until sunt obligatorii la aprobare'}), 400

    try:
        # Preluăm cererea + datele elevului într-un singur join
        row = db.session.execute(
            text(
                "SELECT cr.user_id, cr.carte_id, cr.status, "
                "u.email, u.username, c.titlu, c.autor "
                "FROM cereri_carti cr "
                "JOIN users u ON cr.user_id = u.user_id "
                "JOIN carti c ON cr.carte_id = c.carte_id "
                "WHERE cr.cerere_id = :id"
            ),
            {'id': cerere_id}
        ).fetchone()
        if not row:
            return jsonify({'success': False, 'message': 'Cererea nu a fost găsită'}), 404

        user_id, carte_id, status_vechi, email_elev, nume_elev, titlu, autor = row

        db.session.execute(
            text("UPDATE cereri_carti SET status = :status WHERE cerere_id = :id"),
            {'status': status_nou, 'id': cerere_id}
        )

        # La aprobare înregistrăm împrumutul activ și trimitem email de notificare
        if status_nou == 'approved' and status_vechi != 'approved':
            now = datetime.datetime.utcnow()
            due = now + datetime.timedelta(days=30)
            db.session.execute(
                text(
                    "INSERT INTO imprumuturi_active (user_id, carte_id, data_imprumut, data_scadenta) "
                    "VALUES (:uid, :cid, :now, :due)"
                ),
                {'uid': user_id, 'cid': carte_id, 'now': now, 'due': due}
            )

            # Trimitem emailul de notificare elevului
            html_body = f"""
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: Arial, sans-serif; background: #f5f0e8; margin: 0; padding: 0;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f0e8; padding: 32px 0;">
    <tr><td align="center">
      <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,0.08);">
        <tr>
          <td style="background:#2c3e50; padding: 24px 32px; text-align:center;">
            <h1 style="color:#f5f0e8; margin:0; font-size:22px;">📚 Biblioteca CNI Suceava</h1>
          </td>
        </tr>
        <tr>
          <td style="padding: 32px;">
            <p style="font-size:16px; color:#333; margin-top:0;">Salut, <strong>{nume_elev}</strong>!</p>
            <p style="font-size:15px; color:#333;">Cererea ta de împrumut pentru cartea:</p>
            <div style="background:#f5f0e8; border-left:4px solid #e74c3c; padding:12px 16px; border-radius:6px; margin:16px 0;">
              <strong style="font-size:16px; color:#2c3e50;">„{titlu}"</strong><br>
              <span style="color:#555; font-size:14px;">de {autor}</span>
            </div>
            <p style="font-size:15px; color:#2c3e50; font-weight:bold;">✅ a fost <span style="color:#27ae60;">APROBATĂ</span>!</p>
            <p style="font-size:15px; color:#333;">Poți ridica cartea de la bibliotecă în intervalul:</p>
            <div style="background:#eaf7ec; border:1px solid #a8e6b8; border-radius:8px; padding:14px 20px; margin:16px 0; text-align:center;">
              <span style="font-size:18px; font-weight:bold; color:#1a7a3c;">🕐 {pickup_from_str} — {pickup_until_str}</span>
            </div>
            <p style="font-size:13px; color:#888;">Dacă nu poți ridica cartea în acest interval, te rugăm să contactezi biblioteca.</p>
            <hr style="border:none; border-top:1px solid #eee; margin:24px 0;">
            <p style="font-size:12px; color:#aaa; text-align:center; margin:0;">Biblioteca CNI Suceava · Sistem automat, te rugăm nu răspunde la acest email.</p>
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""
            send_email(
                recipients=[email_elev],
                subject=f'Cerere aprobată: „{titlu}"',
                html_body=html_body
            )

        db.session.commit()
        return jsonify({'success': True, 'message': f'Cerere {status_nou}'}), 200
    except Exception:
        db.session.rollback()
        logger.exception('Eroare la actualizarea cererii %d', cerere_id)
        return jsonify({'success': False, 'message': 'Eroare la actualizarea cererii'}), 500


# ── Raport Word ──────────────────────────────────────────────

@main_bp.route('/librarian/report/docx', methods=['GET'])
@bibliotecar_required
def librarian_report_docx():
    """Generează un raport Word (.docx) cu toți elevii și cărțile citite/împrumutate."""
    try:
        # Toți utilizatorii obișnuiți (elevi)
        students = db.session.execute(
            text("SELECT user_id, username, email FROM users WHERE rol NOT IN ('1','bibliotecar','administrator') ORDER BY username ASC")
        ).fetchall()

        # Cărți citite per utilizator: {user_id: [(titlu, autor), ...]}
        read_rows = db.session.execute(
            text(
                "SELECT cc.user_id, c.titlu, c.autor "
                "FROM carti_citite cc JOIN carti c ON cc.carte_id = c.carte_id"
            )
        ).fetchall()
        read_map = {}
        for r in read_rows:
            read_map.setdefault(r[0], []).append((r[1], r[2]))

        # Împrumuturi active per utilizator: {user_id: [(titlu, autor, data_imprumut, data_scadenta), ...]}
        borrow_rows = db.session.execute(
            text(
                "SELECT ia.user_id, c.titlu, c.autor, ia.data_imprumut, ia.data_scadenta "
                "FROM imprumuturi_active ia JOIN carti c ON ia.carte_id = c.carte_id "
                "ORDER BY ia.data_scadenta ASC"
            )
        ).fetchall()
        borrow_map = {}
        for r in borrow_rows:
            borrow_map.setdefault(r[0], []).append((r[1], r[2], r[3], r[4]))

        # Construim documentul Word
        doc = Document()

        # Titlu
        title_para = doc.add_heading('Raport Bibliotecă – Elevi și Împrumuturi', level=0)
        title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        generated_para = doc.add_paragraph(
            f'Generat la: {datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}'
        )
        generated_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_paragraph()  # spațiu gol

        if not students:
            doc.add_paragraph('Nu există elevi înregistrați.')
        else:
            for uid, username, email in students:
                # Heading elev
                heading = doc.add_heading(username, level=1)
                email_para = doc.add_paragraph()
                email_run = email_para.add_run(f'Email: {email}')
                email_run.italic = True

                # Cărți împrumutate în prezent
                borrows = borrow_map.get(uid, [])
                doc.add_heading('Cărți împrumutate în prezent', level=2)
                if borrows:
                    tbl = doc.add_table(rows=1, cols=4)
                    tbl.style = 'Table Grid'
                    hdr = tbl.rows[0].cells
                    hdr[0].text = 'Titlu'
                    hdr[1].text = 'Autor'
                    hdr[2].text = 'Data împrumutului'
                    hdr[3].text = 'Dată scadentă (30 zile)'
                    for cell in hdr:
                        run = cell.paragraphs[0].runs[0]
                        run.bold = True
                    for titlu, autor, data_imp, data_sc in borrows:
                        row_cells = tbl.add_row().cells
                        row_cells[0].text = titlu
                        row_cells[1].text = autor
                        row_cells[2].text = data_imp.strftime('%d.%m.%Y') if data_imp else '—'
                        row_cells[3].text = data_sc.strftime('%d.%m.%Y') if data_sc else '—'
                else:
                    doc.add_paragraph('Niciun împrumut activ.')

                # Cărți deja citite
                reads = read_map.get(uid, [])
                doc.add_heading('Cărți citite', level=2)
                if reads:
                    tbl2 = doc.add_table(rows=1, cols=2)
                    tbl2.style = 'Table Grid'
                    hdr2 = tbl2.rows[0].cells
                    hdr2[0].text = 'Titlu'
                    hdr2[1].text = 'Autor'
                    for cell in hdr2:
                        run = cell.paragraphs[0].runs[0]
                        run.bold = True
                    for titlu, autor in reads:
                        row_cells = tbl2.add_row().cells
                        row_cells[0].text = titlu
                        row_cells[1].text = autor
                else:
                    doc.add_paragraph('Nicio carte citită înregistrată.')

                doc.add_paragraph()  # spațiu între elevi

        buf = io.BytesIO()
        doc.save(buf)
        buf.seek(0)

        filename = f'raport_biblioteca_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.docx'
        return send_file(
            buf,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    except Exception:
        logger.exception('Eroare la generarea raportului Word')
        return jsonify({'success': False, 'message': 'Eroare la generarea raportului'}), 500


@main_bp.route('/admin/users', methods=['GET'])
@bibliotecar_required
def admin_get_users():
    """Listează toate conturile de utilizatori. Doar bibliotecar."""
    try:
        rows = db.session.execute(
            text("SELECT user_id, username, email, rol, telefon FROM users ORDER BY username ASC")
        ).fetchall()
        users = [
            {
                'user_id': r[0],
                'username': r[1],
                'email': r[2],
                'rol': normalize_role(r[3]),
                'telefon': r[4]
            }
            for r in rows
        ]
        return jsonify({'success': True, 'users': users}), 200
    except Exception:
        logger.exception('Eroare la preluarea listei de utilizatori')
        return jsonify({'success': False, 'error': 'Eroare la preluarea utilizatorilor'}), 500


@main_bp.route('/admin/users/<int:user_id>', methods=['GET'])
@bibliotecar_required
def admin_get_user_detail(user_id):
    """Returnează detalii complete despre un utilizator. Doar bibliotecar."""
    try:
        user_row = db.session.execute(
            text("SELECT user_id, username, email, rol, telefon, description FROM users WHERE user_id = :uid"),
            {'uid': user_id}
        ).fetchone()
        if not user_row:
            return jsonify({'success': False, 'message': 'Utilizatorul nu a fost găsit'}), 404

        # Cărți împrumutate în prezent — sursa autoritativă este imprumuturi_active
        borrowed_rows = db.session.execute(
            text("""
                SELECT c.carte_id, c.titlu, c.autor, c.ISBN,
                       ia.data_imprumut, ia.data_scadenta
                FROM imprumuturi_active ia
                JOIN carti c ON ia.carte_id = c.carte_id
                WHERE ia.user_id = :uid
                ORDER BY ia.data_imprumut DESC
            """),
            {'uid': user_id}
        ).fetchall()

        # Cărți citite / returnate
        read_rows = db.session.execute(
            text("""
                SELECT c.carte_id, c.titlu, c.autor, c.ISBN
                FROM carti_citite cc
                JOIN carti c ON cc.carte_id = c.carte_id
                WHERE cc.user_id = :uid
            """),
            {'uid': user_id}
        ).fetchall()

        # Istoricul complet al cererilor de împrumut
        history_rows = db.session.execute(
            text("""
                SELECT cc.cerere_id, c.titlu, c.autor, cc.status, cc.created_at
                FROM cereri_carti cc
                JOIN carti c ON cc.carte_id = c.carte_id
                WHERE cc.user_id = :uid
                ORDER BY cc.created_at DESC
            """),
            {'uid': user_id}
        ).fetchall()

        # Recenzii scrise de utilizator
        review_rows = db.session.execute(
            text("""
                SELECT r.id, c.titlu, c.autor, r.nota, r.comentariu
                FROM recenzii r
                JOIN carti c ON r.carte_id = c.carte_id
                WHERE r.user_id = :uid
                ORDER BY r.id DESC
            """),
            {'uid': user_id}
        ).fetchall()

        return jsonify({
            'success': True,
            'user': {
                'user_id': user_row[0],
                'username': user_row[1],
                'email': user_row[2],
                'rol': normalize_role(user_row[3]),
                'telefon': user_row[4],
                'description': user_row[5]
            },
            'books_borrowed': [
                {
                    'carte_id': r[0], 'titlu': r[1], 'autor': r[2], 'ISBN': r[3],
                    'borrowed_at': r[4].isoformat() if r[4] else None,
                    'due_at': r[5].isoformat() if r[5] else None
                }
                for r in borrowed_rows
            ],
            'books_read': [
                {'carte_id': r[0], 'titlu': r[1], 'autor': r[2], 'ISBN': r[3]}
                for r in read_rows
            ],
            'borrow_history': [
                {
                    'cerere_id': r[0], 'titlu': r[1], 'autor': r[2],
                    'status': r[3],
                    'created_at': r[4].isoformat() if r[4] else None
                }
                for r in history_rows
            ],
            'reviews': [
                {'id': r[0], 'titlu': r[1], 'autor': r[2], 'nota': r[3], 'comentariu': r[4]}
                for r in review_rows
            ]
        }), 200
    except Exception:
        logger.exception('Eroare la preluarea detaliilor utilizatorului %d', user_id)
        return jsonify({'success': False, 'error': 'Eroare la preluarea detaliilor utilizatorului'}), 500

@main_bp.route('/reviews', methods=['GET'])
def get_reviews():
    """Returnează recenziile pentru o carte dată prin carte_id.
    Include username, nota și comentariu.
    """
    carte_id = request.args.get('carte_id')
    if not carte_id:
        return jsonify({'success': False, 'message': 'carte_id este obligatoriu'}), 400

    try:
        query = text("""
            SELECT r.id, r.nota, r.comentariu, u.username
            FROM recenzii r
            JOIN users u ON r.user_id = u.user_id
            WHERE r.carte_id = :carte_id
            ORDER BY r.id DESC
        """)
        result = db.session.execute(query, {'carte_id': carte_id})
        reviews = []
        for row in result:
            reviews.append({
                'id': row[0],
                'nota': row[1],
                'comentariu': row[2],
                'username': row[3]
            })

        # Calculăm media notelor
        avg_rating = 0
        if reviews:
            avg_rating = round(sum(r['nota'] for r in reviews) / len(reviews), 1)

        return jsonify({
            'success': True,
            'reviews': reviews,
            'avg_rating': avg_rating,
            'total_reviews': len(reviews)
        }), 200
    except Exception:
        logger.exception('Eroare la preluarea recenziilor')
        return jsonify({'success': False, 'error': 'Eroare la preluarea recenziilor'}), 500


@main_bp.route('/reviews', methods=['POST'])
@jwt_required
def submit_review():
    """Salvează o recenzie pentru o carte. Necesită autentificare."""
    user = request.current_user
    data = request.get_json(silent=True) or {}
    carte_id = data.get('carte_id')
    nota = data.get('nota')
    comentariu = (data.get('comentariu') or '').strip()

    if not carte_id or nota is None or not comentariu:
        return jsonify({'success': False, 'message': 'carte_id, nota și comentariu sunt obligatorii'}), 400

    try:
        nota = int(nota)
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': 'nota trebuie să fie un număr întreg 1-5'}), 400

    if nota < 1 or nota > 5:
        return jsonify({'success': False, 'message': 'nota trebuie să fie între 1 și 5'}), 400

    # Verificăm că cartea există
    book = db.session.execute(text("SELECT carte_id FROM carti WHERE carte_id = :id"), {'id': carte_id}).fetchone()
    if not book:
        return jsonify({'success': False, 'message': 'Cartea nu a fost găsită'}), 404

    try:
        # Upsert: o recenzie per utilizator per carte
        existing = db.session.execute(
            text("SELECT id FROM recenzii WHERE user_id = :uid AND carte_id = :cid"),
            {'uid': user['user_id'], 'cid': carte_id}
        ).fetchone()

        if existing:
            db.session.execute(
                text("UPDATE recenzii SET nota = :nota, comentariu = :comentariu WHERE id = :id"),
                {'nota': nota, 'comentariu': comentariu, 'id': existing[0]}
            )
        else:
            db.session.execute(
                text("INSERT INTO recenzii (user_id, carte_id, nota, comentariu) VALUES (:uid, :cid, :nota, :com)"),
                {'uid': user['user_id'], 'cid': carte_id, 'nota': nota, 'com': comentariu}
            )
        db.session.commit()
        return jsonify({'success': True, 'message': 'Recenzie salvată'}), 200
    except Exception:
        db.session.rollback()
        logger.exception('Eroare la salvarea recenziei')
        return jsonify({'success': False, 'message': 'Eroare la salvarea recenziei'}), 500


@main_bp.route('/reviews/user', methods=['GET'])
@jwt_required
def get_user_reviews():
    """Returnează toate recenziile scrise de utilizatorul autentificat."""
    user_id = request.current_user['user_id']

    try:
        query = text("""
            SELECT r.id, r.nota, r.comentariu, c.titlu, c.autor
            FROM recenzii r
            JOIN carti c ON r.carte_id = c.carte_id
            WHERE r.user_id = :user_id
            ORDER BY r.id DESC
        """)
        result = db.session.execute(query, {'user_id': user_id})
        reviews = [
            {'id': row[0], 'nota': row[1], 'comentariu': row[2], 'titlu': row[3], 'autor': row[4]}
            for row in result
        ]
        return jsonify({'success': True, 'reviews': reviews, 'total_reviews': len(reviews)}), 200
    except Exception:
        logger.exception('Eroare la preluarea recenziilor utilizatorului')
        return jsonify({'success': False, 'error': 'Eroare la preluarea recenziilor'}), 500


# ── Rute autentificare ────────────────────────────────────────
@main_bp.route('/auth/login', methods=['POST'])
def login():
    """Login cu verificare bcrypt a parolei. Setează cookie httpOnly JWT."""
    data = request.get_json(silent=True) or {}
    raw_email = data.get('email')
    parola = data.get('password')

    if not raw_email or not parola:
        return jsonify({'success': False, 'message': 'Email și parola sunt obligatorii'}), 400

    email = normalize_cni_email(raw_email)
    if not email:
        return jsonify({'success': False, 'message': 'Doar emailurile @cni-sv.ro sunt permise'}), 400

    query = text(
        "SELECT user_id, username, email, hashed_password, rol FROM users WHERE email = :email"
    )
    result = db.session.execute(query, {'email': email}).mappings().first()

    if not result:
        return jsonify({'success': False, 'message': 'Credențiale invalide'}), 401

    parola_hash = result.get('hashed_password')
    if not parola_hash or not bcrypt.checkpw(parola.encode('utf-8'), parola_hash.encode('utf-8')):
        return jsonify({'success': False, 'message': 'Credențiale invalide'}), 401

    token = create_jwt_token(
        user_id=result['user_id'],
        username=result['username'],
        email=result['email']
    )

    rol_normalizat = normalize_role(result['rol'])

    resp = jsonify({
        'success': True,
        'message': 'Autentificare reușită',
        'user': {
            'user_id': result['user_id'],
            'username': result['username'],
            'email': result['email'],
            'rol': rol_normalizat
        }
    })
    set_jwt_cookie(resp, token)
    return resp, 200

@main_bp.route('/auth/me', methods=['GET'])
@jwt_required
def auth_me():
    """Returnează utilizatorul autentificat curent din cookie-ul JWT."""
    user = request.current_user
    return jsonify({
        'success': True,
        'user_id': user['user_id'],
        'username': user['username'],
        'email': user['email'],
        'rol': user['rol']
    }), 200


@main_bp.route('/auth/logout', methods=['POST'])
def logout():
    """Șterge cookie-ul JWT."""
    resp = jsonify({'success': True, 'message': 'Deconectat cu succes'})
    clear_jwt_cookie(resp)
    return resp, 200


@main_bp.route('/auth/profile', methods=['GET'])
@jwt_required
def profile():
    """Returnează informațiile de profil din sesiunea JWT."""
    user = request.current_user

    query = text(
        "SELECT user_id, username, email, description FROM users WHERE user_id = :user_id"
    )
    result = db.session.execute(query, {'user_id': user['user_id']}).mappings().first()
    if not result:
        return jsonify({'success': False, 'message': 'Profilul nu a fost găsit'}), 404

    return jsonify({
        'success': True,
        'user_id': result.get('user_id'),
        'username': result.get('username'),
        'email': result.get('email'),
        'description': result.get('description')
    }), 200

@main_bp.route('/auth/books-read', methods=['GET'])
@jwt_required
def books_read():
    """Returnează cărțile citite de utilizatorul autentificat."""
    user = request.current_user
    user_id = user['user_id']

    query = text(
        "SELECT c.carte_id, c.titlu, c.autor, c.ISBN "
        "FROM carti_citite cc "
        "JOIN carti c ON cc.carte_id = c.carte_id "
        "WHERE cc.user_id = :user_id"
    )
    rows = db.session.execute(query, {'user_id': user_id}).mappings().all()

    books = []
    for row in rows:
        books.append({
            'carte_id': row.get('carte_id'),
            'titlu': row.get('titlu'),
            'autor': row.get('autor'),
            'ISBN': row.get('ISBN')
        })

    return jsonify({'success': True, 'books': books}), 200

@main_bp.route('/auth/profile', methods=['PUT'])
@jwt_required
def update_profile():
    """Actualizează descrierea utilizatorului autentificat."""
    user = request.current_user
    data = request.get_json(silent=True) or {}
    description = data.get('description')

    update_query = text(
        "UPDATE users SET description = :description WHERE user_id = :user_id"
    )
    try:
        result = db.session.execute(update_query, {'description': description, 'user_id': user['user_id']})
        db.session.commit()
        if result.rowcount == 0:
            return jsonify({'success': False, 'message': 'Profilul nu a fost găsit'}), 404
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Eroare la actualizarea descrierii'}), 500

    return jsonify({'success': True, 'message': 'Descriere actualizată'}), 200

@main_bp.route('/auth/register', methods=['POST'])
def register():
    """Înregistrare cu hashing bcrypt al parolei. Setează cookie JWT la succes."""
    data = request.get_json(silent=True) or {}
    username = data.get('user') or data.get('username') or data.get('fullName')
    raw_email = data.get('email')
    parola = data.get('password')

    if not username or not raw_email or not parola:
        return jsonify({'success': False, 'message': 'Username, email și parola sunt obligatorii'}), 400

    email = normalize_cni_email(raw_email)
    if not email:
        return jsonify({'success': False, 'message': 'Doar emailurile @cni-sv.ro sunt permise'}), 400

    if len(parola) < 8:
        return jsonify({'success': False, 'message': 'Parola trebuie să aibă cel puțin 8 caractere'}), 400

    parola_hash = bcrypt.hashpw(parola.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    values = {
        'username': username,
        'email': email,
        'hashed_password': parola_hash,
        'rol': 'user',
        'telefon': None
    }

    insert_query = text(
        "INSERT INTO users (username, email, hashed_password, rol, telefon) VALUES (:username, :email, :hashed_password, :rol, :telefon)"
    )

    try:
        db.session.execute(insert_query, values)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Username sau email deja existente'}), 409
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Înregistrarea a eșuat'}), 500

    # Preluăm noul user_id ca să putem emite un token
    query = text("SELECT user_id FROM users WHERE email = :email")
    new_user = db.session.execute(query, {'email': email}).mappings().first()
    token = create_jwt_token(
        user_id=new_user['user_id'],
        username=username,
        email=email
    )

    resp = jsonify({'success': True, 'message': 'Înregistrare reușită'})
    set_jwt_cookie(resp, token)
    return resp, 201


@main_bp.route('/auth/profile-picture', methods=['POST'])
@jwt_required
def upload_profile_picture():
    """Încarcă sau înlocuiește poza de profil a utilizatorului.
    Așteaptă multipart/form-data cu câmpul 'file'. Utilizatorul e dedus din JWT.
    """
    user = request.current_user

    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'Niciun fișier trimis'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'Niciun fișier selectat'}), 400

    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'Tip de fișier nepermis. Folosește png, jpg, jpeg, gif sau webp'}), 400

    username = user['username']
    ext = file.filename.rsplit('.', 1)[1].lower()

    # Ștergem poza de profil existentă pentru acest utilizator
    for poza_veche in _find_files_by_prefix(PROFILE_PICTURES_DIR, username):
        os.remove(os.path.join(PROFILE_PICTURES_DIR, poza_veche))

    # Salvăm noul fișier ca username.ext
    filename = f"{username}.{ext}"
    filepath = os.path.join(PROFILE_PICTURES_DIR, filename)
    file.save(filepath)

    return jsonify({
        'success': True,
        'message': 'Poză de profil încărcată',
        'filename': filename
    }), 200


@main_bp.route('/auth/profile-picture/<username>', methods=['GET'])
def get_profile_picture(username):
    """Serve0219te poza de profil a unui utilizator dup0103 username.
    Caut0103 <username>.* 00een folderul profile_pictures.
    """
    matches = _find_files_by_prefix(PROFILE_PICTURES_DIR, username)

    if not rezultate:
        return jsonify({'success': False, 'message': 'No profile picture found'}), 404

    return send_from_directory(PROFILE_PICTURES_DIR, rezultate[0])


@main_bp.route('/books/image', methods=['POST'])
@bibliotecar_required
def upload_book_image():
    """Încarcă sau înlocuiește coperta unei cărți.
    Așteaptă multipart/form-data cu câmpurile 'file' și 'carte_id'.
    Salvează ca <carte_id>.<ext> în folderul book_images.
    """
    carte_id = request.form.get('carte_id')
    if not carte_id:
        return jsonify({'success': False, 'message': 'carte_id is required'}), 400

    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'Niciun fișier trimis'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'Niciun fișier selectat'}), 400

    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'Tip de fișier nepermis. Folosește png, jpg, jpeg, gif sau webp'}), 400

    # Verificăm că cartea există
    query = text("SELECT carte_id FROM carti WHERE carte_id = :carte_id")
    result = db.session.execute(query, {'carte_id': carte_id}).mappings().first()
    if not result:
        return jsonify({'success': False, 'message': 'Cartea nu a fost găsită'}), 404

    ext = file.filename.rsplit('.', 1)[1].lower()

    # Ștergem coperta existentă a cărții
    for imagine_veche in _find_files_by_prefix(BOOK_IMAGES_DIR, str(carte_id)):
        os.remove(os.path.join(BOOK_IMAGES_DIR, imagine_veche))

    # Salvăm noul fișier ca carte_id.ext
    filename = f"{carte_id}.{ext}"
    filepath = os.path.join(BOOK_IMAGES_DIR, filename)
    file.save(filepath)

    return jsonify({
        'success': True,
        'message': 'Copertă carte încărcată',
        'filename': filename
    }), 200


@main_bp.route('/books/image/<int:carte_id>', methods=['GET'])
def get_book_image(carte_id):
    """Servește coperta cărții după carte_id.
    Caută <carte_id>.* în folderul book_images.
    """
    matches = _find_files_by_prefix(BOOK_IMAGES_DIR, str(carte_id))

    if not rezultate:
        return jsonify({'success': False, 'message': 'Nicio imagine găsită'}), 404

    return send_from_directory(BOOK_IMAGES_DIR, rezultate[0])


# ── Rute anunțuri ──────────────────────────────────────

@main_bp.route('/anunturi', methods=['GET'])
def get_anunturi():
    """Returnează toate anunțurile, cel mai nou primul. Include dacă utilizatorul curent a apreciat fiecare."""
    user = get_current_user()
    user_id = user['user_id'] if user else None

    try:
        query = text("""
            SELECT a.anunt_id, a.titlu, a.anunt, a.data_publicare, a.aprecieri
            FROM anunturi a
            ORDER BY a.data_publicare DESC
        """)
        rows = db.session.execute(query).fetchall()

        liked_set = set()
        if user_id:
            liked_rows = db.session.execute(
                text("SELECT anunt_id FROM anunturi_aprecieri WHERE user_id = :uid"),
                {'uid': user_id}
            ).fetchall()
            liked_set = {r[0] for r in liked_rows}

        anunturi = []
        for row in rows:
            anunturi.append({
                'anunt_id': row[0],
                'titlu': row[1],
                'anunt': row[2],
                'data_publicare': row[3].strftime('%d %B %Y, %H:%M') if row[3] else None,
                'aprecieri': row[4] or 0,
                'liked': row[0] in liked_set
            })

        return jsonify({'success': True, 'anunturi': anunturi}), 200
    except Exception:
        logger.exception('Eroare la preluarea anunțurilor')
        return jsonify({'success': False, 'error': 'Eroare la preluarea anunțurilor'}), 500


@main_bp.route('/anunturi', methods=['POST'])
@bibliotecar_required
def create_anunt():
    """Creează un anunț nou. Necesită rol de bibliotecar."""
    data = request.get_json(silent=True) or {}
    titlu = data.get('titlu', '').strip()
    anunt = data.get('anunt', '').strip()

    if not titlu or not anunt:
        return jsonify({'success': False, 'message': 'titlu și anunt sunt obligatorii'}), 400

    try:
        db.session.execute(
            text("INSERT INTO anunturi (titlu, anunt, data_publicare, aprecieri) VALUES (:titlu, :anunt, NOW(), 0)"),
            {'titlu': titlu, 'anunt': anunt}
        )
        db.session.commit()
        return jsonify({'success': True, 'message': 'Anunț creat'}), 201
    except Exception:
        db.session.rollback()
        logger.exception('Eroare la crearea anunțului')
        return jsonify({'success': False, 'message': 'Eroare la crearea anunțului'}), 500


@main_bp.route('/anunturi/<int:anunt_id>', methods=['PUT'])
@bibliotecar_required
def update_anunt(anunt_id):
    """Actualizează un anunț. Necesită rol de bibliotecar."""
    data = request.get_json(silent=True) or {}

    fields = {}
    for key in ALLOWED_ANUNT_FIELDS:
        if key in data and data[key] is not None:
            fields[key] = data[key].strip()

    if not fields:
        return jsonify({'success': False, 'message': 'Niciun câmp de actualizat'}), 400

    set_clause = ', '.join(f"{k} = :{k}" for k in fields)
    fields['anunt_id'] = anunt_id

    try:
        result = db.session.execute(text(f"UPDATE anunturi SET {set_clause} WHERE anunt_id = :anunt_id"), fields)
        db.session.commit()
        if result.rowcount == 0:
            return jsonify({'success': False, 'message': 'Anunțul nu a fost găsit'}), 404
        return jsonify({'success': True, 'message': 'Anunț actualizat'}), 200
    except Exception:
        db.session.rollback()
        logger.exception('Eroare la actualizarea anunțului %d', anunt_id)
        return jsonify({'success': False, 'message': 'Eroare la actualizarea anunțului'}), 500


@main_bp.route('/anunturi/<int:anunt_id>', methods=['DELETE'])
@bibliotecar_required
def delete_anunt(anunt_id):
    """Șterge un anunț. Necesită rol de bibliotecar. Șterge și aprecierile asociate."""
    try:
        result = db.session.execute(text("DELETE FROM anunturi WHERE anunt_id = :id"), {'id': anunt_id})
        db.session.commit()
        if result.rowcount == 0:
            return jsonify({'success': False, 'message': 'Announcement not found'}), 404
        return jsonify({'success': True, 'message': 'Anunț șters'}), 200
    except Exception:
        db.session.rollback()
        logger.exception('Eroare la ștergerea anunțului %d', anunt_id)
        return jsonify({'success': False, 'message': 'Eroare la ștergerea anunțului'}), 500


@main_bp.route('/anunturi/<int:anunt_id>/like', methods=['POST'])
@jwt_required
def toggle_like_anunt(anunt_id):
    """Toggle apreciere pe un anunț. Doar utilizatori autentificați."""
    user = request.current_user
    user_id = user['user_id']

    try:
        existing = db.session.execute(
            text("SELECT id FROM anunturi_aprecieri WHERE anunt_id = :aid AND user_id = :uid"),
            {'aid': anunt_id, 'uid': user_id}
        ).fetchone()

        if existing:
            db.session.execute(
                text("DELETE FROM anunturi_aprecieri WHERE anunt_id = :aid AND user_id = :uid"),
                {'aid': anunt_id, 'uid': user_id}
            )
            db.session.execute(
                text("UPDATE anunturi SET aprecieri = GREATEST(aprecieri - 1, 0) WHERE anunt_id = :aid"),
                {'aid': anunt_id}
            )
            db.session.commit()
            apreciat = False
        else:
            db.session.execute(
                text("INSERT INTO anunturi_aprecieri (anunt_id, user_id) VALUES (:aid, :uid)"),
                {'aid': anunt_id, 'uid': user_id}
            )
            db.session.execute(
                text("UPDATE anunturi SET aprecieri = aprecieri + 1 WHERE anunt_id = :aid"),
                {'aid': anunt_id}
            )
            db.session.commit()
            apreciat = True

        count = db.session.execute(
            text("SELECT aprecieri FROM anunturi WHERE anunt_id = :aid"),
            {'aid': anunt_id}
        ).fetchone()

        return jsonify({'success': True, 'liked': apreciat, 'aprecieri': count[0] if count else 0}), 200
    except Exception:
        db.session.rollback()
        logger.exception('Eroare la toggle apreciere anunț %d', anunt_id)
        return jsonify({'success': False, 'message': 'Eroare la toggle apreciere'}), 500


# ── Helper AI ────────────────────────────────────────────────

GROQ_MODEL = 'llama-3.3-70b-versatile'

def _get_groq_client():
    """Returnează un client Groq, sau None dacă API key-ul lipsește."""
    api_key = current_app.config.get('GROQ_API_KEY', '')
    if not api_key:
        return None
    return Groq(api_key=api_key)

def _groq_chat(client, prompt):
    """Trimite un prompt single-turn către Groq și returnează răspunsul text."""
    logger.info('Prompt Groq: %s', prompt[:300])
    raspuns = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{'role': 'user', 'content': prompt}],
        max_tokens=1024,
        temperature=0.7
    )
    return raspuns.choices[0].message.content.strip()


@main_bp.route('/ai/recommend', methods=['GET'])
@jwt_required
def ai_recommend():
    """Returnează recomandări personalizate de cărți bazate pe istoricul de citire."""
    user = request.current_user
    user_id = user['user_id']

    client = _get_groq_client()
    if not client:
        return jsonify({'success': False, 'message': 'AI neconfigurat'}), 503

    try:
        # Toate cărțile din bibliotecă cu disponibilitate reală
        all_rows = db.session.execute(
            text("SELECT carte_id, titlu, autor, gen, stoc_disponibil FROM carti ORDER BY titlu")
        ).fetchall()

        # Cărțile pe care utilizatorul le-a citit/returnat deja
        read_rows = db.session.execute(
            text("SELECT c.carte_id, c.titlu, c.autor, c.gen FROM carti_citite cc JOIN carti c ON cc.carte_id = c.carte_id WHERE cc.user_id = :uid"),
            {'uid': user_id}
        ).fetchall()

        # Cărțile pe care utilizatorul le are împrumutate sau solicitate
        borrowed_rows = db.session.execute(
            text("SELECT c.carte_id, c.titlu, c.autor FROM cereri_carti cc JOIN carti c ON cc.carte_id = c.carte_id WHERE cc.user_id = :uid AND cc.status IN ('pending', 'approved')"),
            {'uid': user_id}
        ).fetchall()

        if not read_rows:
            return jsonify({'success': True, 'recommendations': '', 'no_history': True}), 200

        already_have_ids = {r[0] for r in read_rows} | {r[0] for r in borrowed_rows}

        read_list = '\n'.join(f'- {r[1]} de {r[2]} (gen: {r[3]})' for r in read_rows)
        borrowed_list = '\n'.join(f'- {r[1]} de {r[2]}' for r in borrowed_rows) or 'niciuna'
        lib_list = '\n'.join(
            f'- [ID:{r[0]}] {r[1]} de {r[2]} (gen: {r[3]}) — {"disponibil" if r[4] > 0 else "indisponibil"}'
            for r in all_rows
        )

        prompt = (
            "Ești bibliotecar la o școală. Ai acces la catalogul COMPLET al bibliotecii de mai jos.\n"
            "Recomandă DOAR cărți care există în catalog și sunt marcate ca 'disponibil'.\n"
            "Nu inventa titluri sau autori care nu sunt în catalog.\n\n"
            f"CATALOG COMPLET AL BIBLIOTECII:\n{lib_list}\n\n"
            f"Cărți citite de elev (nu le recomanda din nou):\n{read_list}\n\n"
            f"Cărți deja împrumutate/solicitate de elev:\n{borrowed_list}\n\n"
            "Recomandă 3-4 cărți disponibile din catalog pe care elevul nu le-a citit și nu le are deja. "
            "Pentru fiecare menționează titlul exact din catalog, autorul și de ce i-ar plăcea elevului (1-2 propoziții). "
            "Răspunde în română, prietenos."
        )

        raspuns_ai = _groq_chat(client, prompt)
        return jsonify({'success': True, 'recommendations': raspuns_ai}), 200
    except Exception:
        logger.exception('Eroare AI recommend')
        return jsonify({'success': False, 'message': 'Cererea AI a eșuat'}), 500


@main_bp.route('/ai/review-assist', methods=['POST'])
@jwt_required
def ai_review_assist():
    """Reformulează o ciornă de recenzie într-o recenzie bine scrisă."""
    data = request.get_json(silent=True) or {}
    ciorna = (data.get('draft') or '').strip()
    titlu_carte = (data.get('titlu') or '').strip()
    nota_raw = data.get('nota', 0)

    if not ciorna:
        return jsonify({'success': False, 'message': 'ciorna (draft) este obligatorie'}), 400

    client = _get_groq_client()
    if not client:
        return jsonify({'success': False, 'message': 'AI neconfigurat'}), 503

    try:
        prompt = (
            f"Ești un asistent pentru recenzii de carte. Elevul vrea să scrie o recenzie pentru "
            f'"{titlu_carte}" cu nota {nota_raw}/5. Gândul lui brut:\n"{ciorna}"\n\n'
            "Rescrie-l ca o recenzie coerentă, bine scrisă, de 2-4 propoziții. "
            "Păstrează opinia originală, nu adăuga informații inventate. Răspunde DOAR cu textul recenziei, fără explicații."
        )
        raspuns_ai = _groq_chat(client, prompt)
        return jsonify({'success': True, 'review': raspuns_ai}), 200
    except Exception:
        logger.exception('Eroare AI review-assist')
        return jsonify({'success': False, 'message': 'Cererea AI a eșuat'}), 500


@main_bp.route('/ai/book-summary/<int:carte_id>', methods=['GET'])
def ai_book_summary(carte_id):
    """Rezumă recenziile pentru o carte într-un scurt sumar de opinie."""
    client = _get_groq_client()
    if not client:
        return jsonify({'success': False, 'message': 'AI neconfigurat'}), 503

    try:
        book_row = db.session.execute(
            text("SELECT titlu, autor FROM carti WHERE carte_id = :id"), {'id': carte_id}
        ).fetchone()
        if not book_row:
            return jsonify({'success': False, 'message': 'Cartea nu a fost găsită'}), 404

        reviews = db.session.execute(
            text("SELECT nota, comentariu FROM recenzii WHERE carte_id = :id LIMIT 20"), {'id': carte_id}
        ).fetchall()

        if not reviews:
            return jsonify({'success': True, 'summary': '', 'no_reviews': True}), 200

        review_text = '\n'.join(f'- Nota {r[0]}/5: {r[1]}' for r in reviews)
        prompt = (
            f'Carte: "{book_row[0]}" de {book_row[1]}\n'
            f"Recenzii de la cititori:\n{review_text}\n\n"
            "Scrie un rezumat de 2-3 propoziții al opiniei generale a cititorilor despre această carte. "
            "Menționează dacă e apreciată sau nu și de ce. Răspunde în română."
        )
        raspuns_ai = _groq_chat(client, prompt)
        return jsonify({'success': True, 'summary': raspuns_ai}), 200
    except Exception:
        logger.exception('Eroare AI book-summary pentru carte_id=%d', carte_id)
        return jsonify({'success': False, 'message': 'Cererea AI a eșuat'}), 500


@main_bp.route('/ai/chat', methods=['POST'])
def ai_chat():
    """Chatbot general al bibliotecii. Răspunde la întrebări folosind contextul bibliotecii."""
    data = request.get_json(silent=True) or {}
    message = (data.get('message') or '').strip()
    if not message:
        return jsonify({'success': False, 'message': 'mesajul este obligatoriu'}), 400

    client = _get_groq_client()
    if not client:
        return jsonify({'success': False, 'message': 'AI neconfigurat'}), 503

    try:
        # Catalogul complet din DB
        books = db.session.execute(
            text("SELECT carte_id, titlu, autor, gen, stoc_disponibil FROM carti ORDER BY titlu")
        ).fetchall()
        book_list = '\n'.join(
            f'- [ID:{r[0]}] {r[1]} de {r[2]} (gen: {r[3]}) — {"disponibil" if r[4] > 0 else "indisponibil"}'
            for r in books
        )

        # Dacă utilizatorul e autentificat, adăugăm contextul său de citire
        user = get_current_user()
        context_utilizator = ''
        if user:
            read_rows = db.session.execute(
                text("SELECT c.titlu, c.autor FROM carti_citite cc JOIN carti c ON cc.carte_id = c.carte_id WHERE cc.user_id = :uid"),
                {'uid': user['user_id']}
            ).fetchall()
            if read_rows:
                context_utilizator = '\nCărți citite de utilizatorul curent: ' + ', '.join(f'"{r[0]}"' for r in read_rows) + '\n'

        prompt = (
            "Ești asistentul virtual al bibliotecii școlii CNI Suceava. "
            "Răspunzi scurt, prietenos și în română. "
            "Folosește DOAR informațiile din catalogul de mai jos — nu inventa cărți sau autori.\n\n"
            f"CATALOG COMPLET:\n{book_list}\n"
            f"{context_utilizator}\n"
            f"Întrebarea utilizatorului: {message}"
        )
        raspuns_ai = _groq_chat(client, prompt)
        return jsonify({'success': True, 'reply': raspuns_ai}), 200
    except Exception:
        logger.exception('Eroare AI chat')
        return jsonify({'success': False, 'message': 'Cererea AI a eșuat'}), 500
