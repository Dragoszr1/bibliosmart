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
from docx.shared import Pt, RGBColor, Inches
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
ALLOWED_BOOK_FIELDS = frozenset({'titlu', 'autor', 'ISBN', 'stoc_total', 'stoc_disponibil', 'gen'})
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
    """Safely find files in directory matching prefix.<allowed_ext>.
    Uses os.listdir instead of glob to avoid glob injection from
    user-controlled strings containing *, ?, or [] characters.
    """
    os.makedirs(directory, exist_ok=True)
    matches = []
    for entry in os.listdir(directory):
        if not entry.startswith(prefix + '.'):
            continue
        ext = entry.rsplit('.', 1)[1].lower() if '.' in entry else ''
        if ext in ALLOWED_EXTENSIONS:
            matches.append(entry)
    return matches


# ── Email Helper ─────────────────────────────────────────────

def send_email(recipients, subject, html_body):
    """Send an email via SMTP (Gmail).

    Reads SMTP_* settings from the current Flask app config.
    Returns True on success, False on failure (logged, never raises).
    """
    cfg = current_app.config
    host = cfg.get('SMTP_HOST', 'smtp.gmail.com')
    port = cfg.get('SMTP_PORT', 587)
    user = cfg.get('SMTP_USER', '')
    password = cfg.get('SMTP_PASSWORD', '')
    sender = cfg.get('SMTP_FROM', '') or user

    if not user or not password:
        logger.error('SMTP credentials not configured — email not sent')
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
        logger.info('Email sent to %s', recipients)
        return True
    except Exception:
        logger.exception('Failed to send email')
        return False


# ── JWT Helpers ──────────────────────────────────────────────

def normalize_role(raw_role):
    """Normalize legacy role values to the supported set."""
    if raw_role is None:
        return 'user'

    normalized_role = ROLE_ALIASES.get(str(raw_role).strip().lower())
    return normalized_role if normalized_role in VALID_ROLES else 'user'


def normalize_cni_email(email):
    """Return a normalized school email address or None if invalid."""
    if not isinstance(email, str):
        return None

    normalized_email = email.strip().lower()
    if not normalized_email or len(normalized_email) > 254:
        return None

    if not EMAIL_REGEX.fullmatch(normalized_email):
        return None

    local_part, _, domain = normalized_email.rpartition('@')
    if not local_part or '..' in local_part or domain != ALLOWED_EMAIL_DOMAIN:
        return None

    return normalized_email


def fetch_user_by_id(user_id):
    """Load the current user from the database for authorization decisions."""
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
    """Create a JWT token with identity claims only."""
    payload = {
        'user_id': user_id,
        'username': username,
        'email': email,
        'iat': datetime.datetime.now(datetime.timezone.utc),
        'exp': datetime.datetime.now(datetime.timezone.utc) + current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')


def set_jwt_cookie(response, token):
    """Set the JWT token as an httpOnly cookie on the response."""
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
    """Clear the JWT cookie."""
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
    """Decode and verify a JWT token. Returns payload or None."""
    try:
        return jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def get_current_user():
    """Resolve the authenticated user from the JWT cookie and database.
    Caches the result on flask.g so repeated calls in the same request
    don't hit the database again.
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
    """Decorator that enforces a valid JWT cookie."""
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({'success': False, 'message': 'Authentication required'}), 401
        request.current_user = user
        return f(*args, **kwargs)
    return decorated


def role_required(role):
    """Decorator factory that enforces a specific role from the database."""
    if role not in VALID_ROLES:
        raise ValueError(f"Unknown role: {role}")

    def decorator(f):
        @wraps(f)
        @jwt_required
        def decorated(*args, **kwargs):
            if request.current_user.get('rol') != role:
                return jsonify({'success': False, 'message': f'{role.capitalize()} privileges required'}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator


bibliotecar_required = role_required('bibliotecar')

@main_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Server is running'}), 200

@main_bp.route('/', methods=['GET'])
def index():
    """API index"""
    return jsonify({
        'name': 'School Library API',
        'version': '1.0.0',
        'message': 'Database connection established'
    }), 200

# Basic routing structure - queries to be implemented by user
@main_bp.route('/books', methods=['GET'])
def get_books():
    """Get all books from the carti table"""
    try:
        result = db.session.execute(text('SELECT carte_id, titlu, autor, ISBN, stoc_total, stoc_disponibil, imprumutat, gen FROM carti'))
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
                'gen': row[7]
            })
        return jsonify({'books': books}), 200
    except Exception:
        logger.exception('Failed to fetch books')
        return jsonify({'error': 'Failed to fetch books'}), 500


@main_bp.route('/books', methods=['POST'])
@bibliotecar_required
def add_book():
    """Add a new book to the collection. Requires bibliotecar role."""
    data = request.get_json(silent=True) or {}
    titlu = data.get('titlu')
    autor = data.get('autor')
    isbn = data.get('ISBN')
    stoc_total = data.get('stoc_total', 1)
    stoc_disponibil = data.get('stoc_disponibil', stoc_total)
    gen = data.get('gen')

    if not titlu or not autor or not isbn or not gen:
        return jsonify({'success': False, 'message': 'titlu, autor, ISBN, and gen are required'}), 400

    insert_query = text(
        "INSERT INTO carti (titlu, autor, ISBN, stoc_total, stoc_disponibil, imprumutat, gen) "
        "VALUES (:titlu, :autor, :ISBN, :stoc_total, :stoc_disponibil, :imprumutat, :gen)"
    )
    try:
        db.session.execute(insert_query, {
            'titlu': titlu,
            'autor': autor,
            'ISBN': isbn,
            'stoc_total': stoc_total,
            'stoc_disponibil': stoc_disponibil,
            'imprumutat': stoc_disponibil < stoc_total,
            'gen': gen
        })
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'A book with this ISBN already exists'}), 409
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Failed to add book'}), 500

    return jsonify({'success': True, 'message': 'Book added successfully'}), 201


@main_bp.route('/books/<int:carte_id>', methods=['PUT'])
@bibliotecar_required
def update_book(carte_id):
    """Update a book's stock or details. Requires bibliotecar role."""
    data = request.get_json(silent=True) or {}

    # Build dynamic update
    fields = {}
    for key in ALLOWED_BOOK_FIELDS:
        if key in data:
            fields[key] = data[key]

    if not fields:
        return jsonify({'success': False, 'message': 'No fields to update'}), 400

    set_clause = ', '.join(f"{k} = :{k}" for k in fields)
    fields['carte_id'] = carte_id

    # Auto-update imprumutat flag if stock fields are changing
    if 'stoc_total' in fields or 'stoc_disponibil' in fields:
        set_clause += ', imprumutat = (stoc_disponibil < stoc_total)'

    update_query = text(f"UPDATE carti SET {set_clause} WHERE carte_id = :carte_id")
    try:
        result = db.session.execute(update_query, fields)
        db.session.commit()
        if result.rowcount == 0:
            return jsonify({'success': False, 'message': 'Book not found'}), 404
    except IntegrityError:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'ISBN conflict'}), 409
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Failed to update book'}), 500

    return jsonify({'success': True, 'message': 'Book updated successfully'}), 200


@main_bp.route('/books/<int:carte_id>', methods=['DELETE'])
@bibliotecar_required
def delete_book(carte_id):
    """Delete a book from the collection. Requires bibliotecar role."""
    try:
        # Delete related records first
        db.session.execute(text("DELETE FROM recenzii WHERE carte_id = :id"), {'id': carte_id})
        db.session.execute(text("DELETE FROM carti_citite WHERE carte_id = :id"), {'id': carte_id})
        result = db.session.execute(text("DELETE FROM carti WHERE carte_id = :id"), {'id': carte_id})
        db.session.commit()
        if result.rowcount == 0:
            return jsonify({'success': False, 'message': 'Book not found'}), 404
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Failed to delete book'}), 500

    return jsonify({'success': True, 'message': 'Book deleted successfully'}), 200


@main_bp.route('/books/<int:carte_id>/request-fizic', methods=['POST'])
@jwt_required
def request_book_fizic(carte_id):
    """Request a physical copy of a book.

    Sends an email to every user with the 'bibliotecar' role
    informing them that this user wants to pick up the book.
    """
    user = request.current_user

    # Look up the book
    book_row = db.session.execute(
        text("SELECT titlu, autor, stoc_disponibil FROM carti WHERE carte_id = :id"),
        {'id': carte_id}
    ).fetchone()

    if not book_row:
        return jsonify({'success': False, 'message': 'Book not found'}), 404

    titlu, autor, stoc_disponibil = book_row
    if stoc_disponibil <= 0:
        return jsonify({'success': False, 'message': 'Book is not available'}), 409

    # Fetch all librarian emails
    rows = db.session.execute(
        text("SELECT email FROM users WHERE rol = 'bibliotecar'")
    ).fetchall()
    librarian_emails = [r[0] for r in rows if r[0]]

    if not librarian_emails:
        logger.warning('No librarians found to notify for book request %d', carte_id)
        return jsonify({'success': False, 'message': 'No librarians available to process your request'}), 503

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

    # Save the request in the database
    try:
        db.session.execute(
            text("INSERT INTO cereri_carti (user_id, carte_id) VALUES (:uid, :cid)"),
            {'uid': user['user_id'], 'cid': carte_id}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        logger.exception('Failed to save book request to DB')
        return jsonify({'success': False, 'message': 'Failed to save request'}), 500

    # Send email notification (best-effort, don't fail the request if email fails)
    send_email(librarian_emails, subject, html_body)

    return jsonify({'success': True, 'message': 'Cererea a fost trimisă!'}), 200


@main_bp.route('/book-requests', methods=['GET'])
@bibliotecar_required
def get_book_requests():
    """List all book borrow requests. Librarians only."""
    status_filter = request.args.get('status')  # optional: pending, approved, rejected
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
        logger.exception('Failed to fetch book requests')
        return jsonify({'success': False, 'error': 'Failed to fetch requests'}), 500


@main_bp.route('/book-requests/<int:cerere_id>', methods=['PUT'])
@bibliotecar_required
def update_book_request(cerere_id):
    """Approve or reject a book request. Librarians only."""
    data = request.get_json(silent=True) or {}
    new_status = data.get('status')
    if new_status not in ('approved', 'rejected'):
        return jsonify({'success': False, 'message': 'Status must be approved or rejected'}), 400

    # Pickup interval (only required when approving)
    pickup_from_str = (data.get('pickup_from') or '').strip()
    pickup_until_str = (data.get('pickup_until') or '').strip()
    if new_status == 'approved' and (not pickup_from_str or not pickup_until_str):
        return jsonify({'success': False, 'message': 'pickup_from and pickup_until are required when approving'}), 400

    try:
        # Fetch the request + student info in one join
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
            return jsonify({'success': False, 'message': 'Request not found'}), 404

        user_id, carte_id, old_status, student_email, student_name, titlu, autor = row

        db.session.execute(
            text("UPDATE cereri_carti SET status = :status WHERE cerere_id = :id"),
            {'status': new_status, 'id': cerere_id}
        )

        # When approving, record the active borrow and send notification email
        if new_status == 'approved' and old_status != 'approved':
            now = datetime.datetime.utcnow()
            due = now + datetime.timedelta(days=30)
            db.session.execute(
                text(
                    "INSERT INTO imprumuturi_active (user_id, carte_id, data_imprumut, data_scadenta) "
                    "VALUES (:uid, :cid, :now, :due)"
                ),
                {'uid': user_id, 'cid': carte_id, 'now': now, 'due': due}
            )

            # Send email notification to student
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
            <p style="font-size:16px; color:#333; margin-top:0;">Salut, <strong>{student_name}</strong>!</p>
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
                recipients=[student_email],
                subject=f'Cerere aprobată: „{titlu}"',
                html_body=html_body
            )

        db.session.commit()
        return jsonify({'success': True, 'message': f'Request {new_status}'}), 200
    except Exception:
        db.session.rollback()
        logger.exception('Failed to update book request %d', cerere_id)
        return jsonify({'success': False, 'message': 'Failed to update request'}), 500


# ── Word Report ──────────────────────────────────────────────

@main_bp.route('/librarian/report/docx', methods=['GET'])
@bibliotecar_required
def librarian_report_docx():
    """Generate a Word (.docx) report of all students with their read/borrowed books."""
    try:
        # All regular users (students)
        students = db.session.execute(
            text("SELECT user_id, username, email FROM users WHERE rol NOT IN ('1','bibliotecar','administrator') ORDER BY username ASC")
        ).fetchall()

        # Read books per user: {user_id: [(titlu, autor), ...]}
        read_rows = db.session.execute(
            text(
                "SELECT cc.user_id, c.titlu, c.autor "
                "FROM carti_citite cc JOIN carti c ON cc.carte_id = c.carte_id"
            )
        ).fetchall()
        read_map = {}
        for r in read_rows:
            read_map.setdefault(r[0], []).append((r[1], r[2]))

        # Active borrows per user: {user_id: [(titlu, autor, data_imprumut, data_scadenta), ...]}
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

        # Build the document
        doc = Document()

        # Title
        title_para = doc.add_heading('Raport Bibliotecă – Elevi și Împrumuturi', level=0)
        title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        generated_para = doc.add_paragraph(
            f'Generat la: {datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}'
        )
        generated_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_paragraph()  # spacer

        if not students:
            doc.add_paragraph('Nu există elevi înregistrați.')
        else:
            for uid, username, email in students:
                # Student heading
                heading = doc.add_heading(username, level=1)
                email_para = doc.add_paragraph()
                email_run = email_para.add_run(f'Email: {email}')
                email_run.italic = True

                # Currently borrowed books
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

                # Books already read
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

                doc.add_paragraph()  # spacer between students

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
        logger.exception('Failed to generate Word report')
        return jsonify({'success': False, 'message': 'Failed to generate report'}), 500


@main_bp.route('/users', methods=['GET'])
def get_users():
    """Basic users route - implement your queries here"""
    return jsonify({'message': 'Users endpoint - implement your database queries here'}), 200


@main_bp.route('/admin/users', methods=['GET'])
@bibliotecar_required
def admin_get_users():
    """List all user accounts. Bibliotecar only."""
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
        logger.exception('Failed to fetch users list')
        return jsonify({'success': False, 'error': 'Failed to fetch users'}), 500


@main_bp.route('/admin/users/<int:user_id>', methods=['GET'])
@bibliotecar_required
def admin_get_user_detail(user_id):
    """Get full details for a specific user. Bibliotecar only."""
    try:
        user_row = db.session.execute(
            text("SELECT user_id, username, email, rol, telefon, description FROM users WHERE user_id = :uid"),
            {'uid': user_id}
        ).fetchone()
        if not user_row:
            return jsonify({'success': False, 'message': 'User not found'}), 404

        # Books currently borrowed (approved borrow requests)
        borrowed_rows = db.session.execute(
            text("""
                SELECT c.carte_id, c.titlu, c.autor, c.ISBN, cc.created_at
                FROM cereri_carti cc
                JOIN carti c ON cc.carte_id = c.carte_id
                WHERE cc.user_id = :uid AND cc.status = 'approved'
                ORDER BY cc.created_at DESC
            """),
            {'uid': user_id}
        ).fetchall()

        # Books read / returned
        read_rows = db.session.execute(
            text("""
                SELECT c.carte_id, c.titlu, c.autor, c.ISBN
                FROM carti_citite cc
                JOIN carti c ON cc.carte_id = c.carte_id
                WHERE cc.user_id = :uid
            """),
            {'uid': user_id}
        ).fetchall()

        # Full borrow request history
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

        # Reviews
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
                    'borrowed_at': r[4].isoformat() if r[4] else None
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
        logger.exception('Failed to fetch user detail for %d', user_id)
        return jsonify({'success': False, 'error': 'Failed to fetch user details'}), 500

@main_bp.route('/books-read', methods=['GET'])
def get_books_read():
    """Basic books read route - implement your queries here"""
    return jsonify({'message': 'Books read endpoint - implement your database queries here'}), 200

@main_bp.route('/reviews', methods=['GET'])
def get_reviews():
    """Get reviews for a specific book by carte_id.
    Returns reviews with username, nota (rating), and comentariu.
    """
    carte_id = request.args.get('carte_id')
    if not carte_id:
        return jsonify({'success': False, 'message': 'carte_id is required'}), 400

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

        # Calculate average rating
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
        logger.exception('Failed to fetch reviews')
        return jsonify({'success': False, 'error': 'Failed to fetch reviews'}), 500


@main_bp.route('/reviews', methods=['POST'])
@jwt_required
def submit_review():
    """Submit a review for a book. Requires authentication."""
    user = request.current_user
    data = request.get_json(silent=True) or {}
    carte_id = data.get('carte_id')
    nota = data.get('nota')
    comentariu = (data.get('comentariu') or '').strip()

    if not carte_id or nota is None or not comentariu:
        return jsonify({'success': False, 'message': 'carte_id, nota, and comentariu are required'}), 400

    try:
        nota = int(nota)
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': 'nota must be an integer 1-5'}), 400

    if nota < 1 or nota > 5:
        return jsonify({'success': False, 'message': 'nota must be between 1 and 5'}), 400

    # Check book exists
    book = db.session.execute(text("SELECT carte_id FROM carti WHERE carte_id = :id"), {'id': carte_id}).fetchone()
    if not book:
        return jsonify({'success': False, 'message': 'Book not found'}), 404

    try:
        # Upsert: one review per user per book
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
        return jsonify({'success': True, 'message': 'Review submitted'}), 200
    except Exception:
        db.session.rollback()
        logger.exception('Failed to submit review')
        return jsonify({'success': False, 'message': 'Failed to submit review'}), 500


@main_bp.route('/reviews/user', methods=['GET'])
def get_user_reviews():
    """Get all reviews by a specific user.
    Returns reviews with book title, author, nota, and comentariu.
    """
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'user_id is required'}), 400

    try:
        query = text("""
            SELECT r.id, r.nota, r.comentariu, c.titlu, c.autor
            FROM recenzii r
            JOIN carti c ON r.carte_id = c.carte_id
            WHERE r.user_id = :user_id
            ORDER BY r.id DESC
        """)
        result = db.session.execute(query, {'user_id': user_id})
        reviews = []
        for row in result:
            reviews.append({
                'id': row[0],
                'nota': row[1],
                'comentariu': row[2],
                'titlu': row[3],
                'autor': row[4]
            })

        return jsonify({
            'success': True,
            'reviews': reviews,
            'total_reviews': len(reviews)
        }), 200
    except Exception:
        logger.exception('Failed to fetch user reviews')
        return jsonify({'success': False, 'error': 'Failed to fetch reviews'}), 500


# Authentication routes structure
@main_bp.route('/auth/login', methods=['POST'])
def login():
    """Login route with bcrypt password verification. Sets JWT httpOnly cookie."""
    data = request.get_json(silent=True) or {}
    raw_email = data.get('email')
    password = data.get('password')

    if not raw_email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required'}), 400

    email = normalize_cni_email(raw_email)
    if not email:
        return jsonify({'success': False, 'message': 'Doar emailurile @cni-sv.ro sunt permise'}), 400

    query = text(
        "SELECT user_id, username, email, hashed_password, rol FROM users WHERE email = :email"
    )
    result = db.session.execute(query, {'email': email}).mappings().first()

    if not result:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

    hashed_password = result.get('hashed_password')
    if not hashed_password or not bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

    token = create_jwt_token(
        user_id=result['user_id'],
        username=result['username'],
        email=result['email']
    )

    normalized_role = normalize_role(result['rol'])

    resp = jsonify({
        'success': True,
        'message': 'Login successful',
        'user': {
            'user_id': result['user_id'],
            'username': result['username'],
            'email': result['email'],
            'rol': normalized_role
        }
    })
    set_jwt_cookie(resp, token)
    return resp, 200

@main_bp.route('/auth/me', methods=['GET'])
@jwt_required
def auth_me():
    """Return the currently authenticated user from the JWT cookie."""
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
    """Clear the JWT cookie."""
    resp = jsonify({'success': True, 'message': 'Logged out'})
    clear_jwt_cookie(resp)
    return resp, 200


@main_bp.route('/auth/profile', methods=['GET'])
@jwt_required
def profile():
    """Fetch profile information from the JWT session."""
    user = request.current_user

    query = text(
        "SELECT user_id, username, email, description FROM users WHERE user_id = :user_id"
    )
    result = db.session.execute(query, {'user_id': user['user_id']}).mappings().first()
    if not result:
        return jsonify({'success': False, 'message': 'Profile not found'}), 404

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
    """Fetch books read by the authenticated user."""
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
    """Update user description for the authenticated user."""
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
            return jsonify({'success': False, 'message': 'Profile not found'}), 404
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Failed to update description'}), 500

    return jsonify({'success': True, 'message': 'Description updated'}), 200

@main_bp.route('/auth/register', methods=['POST'])
def register():
    """Registration route with bcrypt password hashing. Sets JWT cookie on success."""
    data = request.get_json(silent=True) or {}
    username = data.get('user') or data.get('username') or data.get('fullName')
    raw_email = data.get('email')
    password = data.get('password')

    if not username or not raw_email or not password:
        return jsonify({'success': False, 'message': 'User, email, and password are required'}), 400

    email = normalize_cni_email(raw_email)
    if not email:
        return jsonify({'success': False, 'message': 'Doar emailurile @cni-sv.ro sunt permise'}), 400

    if len(password) < 8:
        return jsonify({'success': False, 'message': 'Password must be at least 8 characters'}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    values = {
        'username': username,
        'email': email,
        'hashed_password': hashed_password,
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
        return jsonify({'success': False, 'message': 'User or email already exists'}), 409
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Registration failed'}), 500

    # Fetch the new user_id so we can issue a token
    query = text("SELECT user_id FROM users WHERE email = :email")
    new_user = db.session.execute(query, {'email': email}).mappings().first()
    token = create_jwt_token(
        user_id=new_user['user_id'],
        username=username,
        email=email
    )

    resp = jsonify({'success': True, 'message': 'Registration successful'})
    set_jwt_cookie(resp, token)
    return resp, 201


@main_bp.route('/auth/profile-picture', methods=['POST'])
@jwt_required
def upload_profile_picture():
    """Upload or replace a user's profile picture.
    Expects multipart/form-data with 'file' field. User determined from JWT.
    """
    user = request.current_user

    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'File type not allowed. Use png, jpg, jpeg, gif, or webp'}), 400

    username = user['username']
    ext = file.filename.rsplit('.', 1)[1].lower()

    # Remove any existing profile picture for this user
    for old_file in _find_files_by_prefix(PROFILE_PICTURES_DIR, username):
        os.remove(os.path.join(PROFILE_PICTURES_DIR, old_file))

    # Save the new file as username.ext
    filename = f"{username}.{ext}"
    filepath = os.path.join(PROFILE_PICTURES_DIR, filename)
    file.save(filepath)

    return jsonify({
        'success': True,
        'message': 'Profile picture uploaded',
        'filename': filename
    }), 200


@main_bp.route('/auth/profile-picture/<username>', methods=['GET'])
def get_profile_picture(username):
    """Serve a user's profile picture by username.
    Looks for <username>.* in the profile_pictures folder.
    """
    matches = _find_files_by_prefix(PROFILE_PICTURES_DIR, username)

    if not matches:
        return jsonify({'success': False, 'message': 'No profile picture found'}), 404

    return send_from_directory(PROFILE_PICTURES_DIR, matches[0])


@main_bp.route('/books/image', methods=['POST'])
@bibliotecar_required
def upload_book_image():
    """Upload or replace a book cover image.
    Expects multipart/form-data with 'file' and 'carte_id' fields.
    Saves as <carte_id>.<ext> in the book_images folder.
    """
    carte_id = request.form.get('carte_id')
    if not carte_id:
        return jsonify({'success': False, 'message': 'carte_id is required'}), 400

    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'File type not allowed. Use png, jpg, jpeg, gif, or webp'}), 400

    # Verify the book exists
    query = text("SELECT carte_id FROM carti WHERE carte_id = :carte_id")
    result = db.session.execute(query, {'carte_id': carte_id}).mappings().first()
    if not result:
        return jsonify({'success': False, 'message': 'Book not found'}), 404

    ext = file.filename.rsplit('.', 1)[1].lower()

    # Remove any existing image for this book
    for old_file in _find_files_by_prefix(BOOK_IMAGES_DIR, str(carte_id)):
        os.remove(os.path.join(BOOK_IMAGES_DIR, old_file))

    # Save the new file as carte_id.ext
    filename = f"{carte_id}.{ext}"
    filepath = os.path.join(BOOK_IMAGES_DIR, filename)
    file.save(filepath)

    return jsonify({
        'success': True,
        'message': 'Book image uploaded',
        'filename': filename
    }), 200


@main_bp.route('/books/image/<int:carte_id>', methods=['GET'])
def get_book_image(carte_id):
    """Serve a book's cover image by carte_id.
    Looks for <carte_id>.* in the book_images folder.
    """
    matches = _find_files_by_prefix(BOOK_IMAGES_DIR, str(carte_id))

    if not matches:
        return jsonify({'success': False, 'message': 'No book image found'}), 404

    return send_from_directory(BOOK_IMAGES_DIR, matches[0])


# ── Announcement Routes ──────────────────────────────────────

@main_bp.route('/anunturi', methods=['GET'])
def get_anunturi():
    """Get all announcements, newest first. Includes whether current user liked each."""
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
        logger.exception('Failed to fetch announcements')
        return jsonify({'success': False, 'error': 'Failed to fetch announcements'}), 500


@main_bp.route('/anunturi', methods=['POST'])
@bibliotecar_required
def create_anunt():
    """Create a new announcement. Requires bibliotecar role."""
    data = request.get_json(silent=True) or {}
    titlu = data.get('titlu', '').strip()
    anunt = data.get('anunt', '').strip()

    if not titlu or not anunt:
        return jsonify({'success': False, 'message': 'titlu and anunt are required'}), 400

    try:
        db.session.execute(
            text("INSERT INTO anunturi (titlu, anunt, data_publicare, aprecieri) VALUES (:titlu, :anunt, NOW(), 0)"),
            {'titlu': titlu, 'anunt': anunt}
        )
        db.session.commit()
        return jsonify({'success': True, 'message': 'Announcement created'}), 201
    except Exception:
        db.session.rollback()
        logger.exception('Failed to create announcement')
        return jsonify({'success': False, 'message': 'Failed to create announcement'}), 500


@main_bp.route('/anunturi/<int:anunt_id>', methods=['PUT'])
@bibliotecar_required
def update_anunt(anunt_id):
    """Update an announcement. Requires bibliotecar role."""
    data = request.get_json(silent=True) or {}

    fields = {}
    for key in ALLOWED_ANUNT_FIELDS:
        if key in data and data[key] is not None:
            fields[key] = data[key].strip()

    if not fields:
        return jsonify({'success': False, 'message': 'No fields to update'}), 400

    set_clause = ', '.join(f"{k} = :{k}" for k in fields)
    fields['anunt_id'] = anunt_id

    try:
        result = db.session.execute(text(f"UPDATE anunturi SET {set_clause} WHERE anunt_id = :anunt_id"), fields)
        db.session.commit()
        if result.rowcount == 0:
            return jsonify({'success': False, 'message': 'Announcement not found'}), 404
        return jsonify({'success': True, 'message': 'Announcement updated'}), 200
    except Exception:
        db.session.rollback()
        logger.exception('Failed to update announcement %d', anunt_id)
        return jsonify({'success': False, 'message': 'Failed to update announcement'}), 500


@main_bp.route('/anunturi/<int:anunt_id>', methods=['DELETE'])
@bibliotecar_required
def delete_anunt(anunt_id):
    """Delete an announcement. Requires bibliotecar role. Cascade deletes likes."""
    try:
        result = db.session.execute(text("DELETE FROM anunturi WHERE anunt_id = :id"), {'id': anunt_id})
        db.session.commit()
        if result.rowcount == 0:
            return jsonify({'success': False, 'message': 'Announcement not found'}), 404
        return jsonify({'success': True, 'message': 'Announcement deleted'}), 200
    except Exception:
        db.session.rollback()
        logger.exception('Failed to delete announcement %d', anunt_id)
        return jsonify({'success': False, 'message': 'Failed to delete announcement'}), 500


@main_bp.route('/anunturi/<int:anunt_id>/like', methods=['POST'])
@jwt_required
def toggle_like_anunt(anunt_id):
    """Toggle like on an announcement. Logged-in users only."""
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
            liked = False
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
            liked = True

        count = db.session.execute(
            text("SELECT aprecieri FROM anunturi WHERE anunt_id = :aid"),
            {'aid': anunt_id}
        ).fetchone()

        return jsonify({'success': True, 'liked': liked, 'aprecieri': count[0] if count else 0}), 200
    except Exception:
        db.session.rollback()
        logger.exception('Failed to toggle like on announcement %d', anunt_id)
        return jsonify({'success': False, 'message': 'Failed to toggle like'}), 500


# ── AI Helper ────────────────────────────────────────────────

GROQ_MODEL = 'llama-3.3-70b-versatile'

def _get_groq_client():
    """Return a Groq client, or None if the API key is missing."""
    api_key = current_app.config.get('GROQ_API_KEY', '')
    if not api_key:
        return None
    return Groq(api_key=api_key)

def _groq_chat(client, prompt):
    """Send a single-turn prompt to Groq and return the text response."""
    logger.info('Groq prompt: %s', prompt[:300])
    resp = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{'role': 'user', 'content': prompt}],
        max_tokens=1024,
        temperature=0.7
    )
    return resp.choices[0].message.content.strip()


@main_bp.route('/ai/recommend', methods=['GET'])
@jwt_required
def ai_recommend():
    """Return personalised book recommendations based on read history."""
    user = request.current_user
    user_id = user['user_id']

    client = _get_groq_client()
    if not client:
        return jsonify({'success': False, 'message': 'AI not configured'}), 503

    try:
        # All books in the library with real availability
        all_rows = db.session.execute(
            text("SELECT carte_id, titlu, autor, gen, stoc_disponibil FROM carti ORDER BY titlu")
        ).fetchall()

        # Books the user has already read/returned
        read_rows = db.session.execute(
            text("SELECT c.carte_id, c.titlu, c.autor, c.gen FROM carti_citite cc JOIN carti c ON cc.carte_id = c.carte_id WHERE cc.user_id = :uid"),
            {'uid': user_id}
        ).fetchall()

        # Books the user currently has borrowed or requested
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

        reply = _groq_chat(client, prompt)
        return jsonify({'success': True, 'recommendations': reply}), 200
    except Exception:
        logger.exception('AI recommend failed')
        return jsonify({'success': False, 'message': 'AI request failed'}), 500


@main_bp.route('/ai/review-assist', methods=['POST'])
@jwt_required
def ai_review_assist():
    """Polish a rough review draft into a well-written review."""
    data = request.get_json(silent=True) or {}
    draft = (data.get('draft') or '').strip()
    book_title = (data.get('titlu') or '').strip()
    rating = data.get('nota', 0)

    if not draft:
        return jsonify({'success': False, 'message': 'draft is required'}), 400

    client = _get_groq_client()
    if not client:
        return jsonify({'success': False, 'message': 'AI not configured'}), 503

    try:
        prompt = (
            f"Ești un asistent pentru recenzii de carte. Elevul vrea să scrie o recenzie pentru "
            f'"{book_title}" cu nota {rating}/5. Gândul lui brut:\n"{draft}"\n\n'
            "Rescrie-l ca o recenzie coerentă, bine scrisă, de 2-4 propoziții. "
            "Păstrează opinia originală, nu adăuga informații inventate. Răspunde DOAR cu textul recenziei, fără explicații."
        )
        reply = _groq_chat(client, prompt)
        return jsonify({'success': True, 'review': reply}), 200
    except Exception:
        logger.exception('AI review-assist failed')
        return jsonify({'success': False, 'message': 'AI request failed'}), 500


@main_bp.route('/ai/book-summary/<int:carte_id>', methods=['GET'])
def ai_book_summary(carte_id):
    """Summarise all reviews for a book into a short opinion summary."""
    client = _get_groq_client()
    if not client:
        return jsonify({'success': False, 'message': 'AI not configured'}), 503

    try:
        book_row = db.session.execute(
            text("SELECT titlu, autor FROM carti WHERE carte_id = :id"), {'id': carte_id}
        ).fetchone()
        if not book_row:
            return jsonify({'success': False, 'message': 'Book not found'}), 404

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
        reply = _groq_chat(client, prompt)
        return jsonify({'success': True, 'summary': reply}), 200
    except Exception:
        logger.exception('AI book-summary failed for carte_id=%d', carte_id)
        return jsonify({'success': False, 'message': 'AI request failed'}), 500


@main_bp.route('/ai/chat', methods=['POST'])
def ai_chat():
    """General library chatbot. Answers questions using library context."""
    data = request.get_json(silent=True) or {}
    message = (data.get('message') or '').strip()
    if not message:
        return jsonify({'success': False, 'message': 'message is required'}), 400

    client = _get_groq_client()
    if not client:
        return jsonify({'success': False, 'message': 'AI not configured'}), 503

    try:
        # Full library catalog from DB
        books = db.session.execute(
            text("SELECT carte_id, titlu, autor, gen, stoc_disponibil FROM carti ORDER BY titlu")
        ).fetchall()
        book_list = '\n'.join(
            f'- [ID:{r[0]}] {r[1]} de {r[2]} (gen: {r[3]}) — {"disponibil" if r[4] > 0 else "indisponibil"}'
            for r in books
        )

        # If user is logged in, add their reading context
        user = get_current_user()
        user_context = ''
        if user:
            read_rows = db.session.execute(
                text("SELECT c.titlu, c.autor FROM carti_citite cc JOIN carti c ON cc.carte_id = c.carte_id WHERE cc.user_id = :uid"),
                {'uid': user['user_id']}
            ).fetchall()
            if read_rows:
                user_context = '\nCărți citite de utilizatorul curent: ' + ', '.join(f'"{r[0]}"' for r in read_rows) + '\n'

        prompt = (
            "Ești asistentul virtual al bibliotecii școlii CNI Suceava. "
            "Răspunzi scurt, prietenos și în română. "
            "Folosește DOAR informațiile din catalogul de mai jos — nu inventa cărți sau autori.\n\n"
            f"CATALOG COMPLET:\n{book_list}\n"
            f"{user_context}\n"
            f"Întrebarea utilizatorului: {message}"
        )
        reply = _groq_chat(client, prompt)
        return jsonify({'success': True, 'reply': reply}), 200
    except Exception:
        logger.exception('AI chat failed')
        return jsonify({'success': False, 'message': 'AI request failed'}), 500
