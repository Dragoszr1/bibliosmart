from flask import request, jsonify, send_from_directory
from sqlalchemy import text
from app.database import db
from app.models import Carti
from app.utils.constants import ALLOWED_BOOK_FIELDS, BOOK_IMAGES_DIR, BOOK_PDFS_DIR
from app.utils.file_utils import allowed_file, _find_files_by_prefix
from app.utils.email_utils import send_email
from sqlalchemy.exc import IntegrityError
import datetime
import os
import logging

logger = logging.getLogger(__name__)

def get_books():
    try:
        result = db.session.execute(text('SELECT carte_id, titlu, autor, ISBN, stoc_total, stoc_disponibil, imprumutat, gen, pozitie, cod FROM carti'))
        os.makedirs(BOOK_PDFS_DIR, exist_ok=True)
        pdf_ids = {f.rsplit('.', 1)[0] for f in os.listdir(BOOK_PDFS_DIR) if f.endswith('.pdf')}
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
                'pozitie': row[8],
                'cod': row[9],
                'has_pdf': str(row[0]) in pdf_ids
            })
        return jsonify({'books': books}), 200
    except Exception:
        logger.exception('Eroare la preluarea cărților')
        return jsonify({'error': 'Eroare la preluarea cărților'}), 500

def get_recent_books():
    try:
        result = db.session.execute(text('SELECT carte_id, titlu, autor, gen, stoc_disponibil FROM carti ORDER BY carte_id DESC LIMIT 3'))
        
        books = []
        for row in result:
            books.append({
                'carte_id': row[0],
                'titlu': row[1],
                'autor': row[2],
                'gen': row[3],
                'stoc_disponibil': row[4]
            })
            
        return jsonify({'success': True, 'books': books}), 200
    except Exception:
        logger.exception('Eroare la preluarea cărților recente')
        return jsonify({'success': False, 'message': 'Eroare la preluarea cărților recente'}), 500

def add_book():
    data = request.get_json(silent=True) or {}
    titlu = data.get('titlu')
    autor = data.get('autor')
    isbn = data.get('ISBN')
    stoc_total = data.get('stoc_total', 1)
    stoc_disponibil = data.get('stoc_disponibil', stoc_total)
    gen = data.get('gen')
    pozitie = data.get('pozitie') or None
    cod = data.get('cod') or None

    if not titlu or not autor or not isbn or not gen:
        return jsonify({'success': False, 'message': 'titlu, autor, ISBN și gen sunt obligatorii'}), 400

    titlu = str(titlu).strip()
    autor = str(autor).strip()
    isbn = str(isbn).strip().replace('-', '').replace(' ', '')
    gen = str(gen).strip()

    if not titlu or len(titlu) > 50:
        return jsonify({'success': False, 'message': 'Titlul nu poate fi gol și trebuie să aibă maximum 50 de caractere'}), 400
    if not autor or len(autor) > 50:
        return jsonify({'success': False, 'message': 'Autorul nu poate fi gol și trebuie să aibă maximum 50 de caractere'}), 400
    if not isbn or len(isbn) not in (10, 13) or not isbn.isalnum():
        return jsonify({'success': False, 'message': 'ISBN-ul trebuie să aibă 10 sau 13 caractere alfanumerice'}), 400
    if not gen or len(gen) > 255:
        return jsonify({'success': False, 'message': 'Genul nu poate fi gol și trebuie să aibă maximum 255 de caractere'}), 400

    if pozitie:
        pozitie = str(pozitie).strip()
        if len(pozitie) > 100:
            return jsonify({'success': False, 'message': 'Poziția trebuie să aibă maximum 100 de caractere'}), 400
    if cod:
        cod = str(cod).strip()
        if len(cod) > 50:
            return jsonify({'success': False, 'message': 'Codul trebuie să aibă maximum 50 de caractere'}), 400

    try:
        stoc_total = int(stoc_total)
        stoc_disponibil = int(stoc_disponibil)
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': 'Stocul total și disponibil trebuie să fie numere întregi'}), 400

    if stoc_total < 0 or stoc_disponibil < 0 or stoc_disponibil > stoc_total:
        return jsonify({'success': False, 'message': 'Stocul total/disponibil invalid'}), 400

    insert_query = text(
        "INSERT INTO carti (titlu, autor, ISBN, stoc_total, stoc_disponibil, imprumutat, gen, pozitie, cod) "
        "VALUES (:titlu, :autor, :ISBN, :stoc_total, :stoc_disponibil, :imprumutat, :gen, :pozitie, :cod)"
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
            'pozitie': pozitie,
            'cod': cod
        })
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Există deja o carte cu acest ISBN'}), 409
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Eroare la adăugarea cărții'}), 500

    return jsonify({'success': True, 'message': 'Carte adăugată cu succes'}), 201

def update_book(carte_id):
    data = request.get_json(silent=True) or {}

    fields = {}
    for key in ALLOWED_BOOK_FIELDS:
        if key in data:
            fields[key] = data[key]

    if not fields:
        return jsonify({'success': False, 'message': 'Niciun câmp de actualizat'}), 400

    if 'titlu' in fields:
        fields['titlu'] = str(fields['titlu']).strip()
        if not fields['titlu'] or len(fields['titlu']) > 50:
            return jsonify({'success': False, 'message': 'Titlul nu poate fi gol și trebuie să aibă maximum 50 de caractere'}), 400
    if 'autor' in fields:
        fields['autor'] = str(fields['autor']).strip()
        if not fields['autor'] or len(fields['autor']) > 50:
            return jsonify({'success': False, 'message': 'Autorul nu poate fi gol și trebuie să aibă maximum 50 de caractere'}), 400
    if 'ISBN' in fields:
        isbn = str(fields['ISBN']).strip().replace('-', '').replace(' ', '')
        if not isbn or len(isbn) not in (10, 13) or not isbn.isalnum():
            return jsonify({'success': False, 'message': 'ISBN-ul trebuie să aibă 10 sau 13 caractere alfanumerice'}), 400
        fields['ISBN'] = isbn
    if 'gen' in fields:
        fields['gen'] = str(fields['gen']).strip()
        if not fields['gen'] or len(fields['gen']) > 255:
            return jsonify({'success': False, 'message': 'Genul nu poate fi gol și trebuie să aibă maximum 255 de caractere'}), 400
    if 'pozitie' in fields:
        if fields['pozitie']:
            fields['pozitie'] = str(fields['pozitie']).strip()
            if len(fields['pozitie']) > 100:
                return jsonify({'success': False, 'message': 'Poziția trebuie să aibă maximum 100 de caractere'}), 400
    if 'cod' in fields:
        if fields['cod']:
            fields['cod'] = str(fields['cod']).strip()
            if len(fields['cod']) > 50:
                return jsonify({'success': False, 'message': 'Codul trebuie să aibă maximum 50 de caractere'}), 400

    if 'stoc_total' in fields or 'stoc_disponibil' in fields:
        book_row = db.session.execute(
            text("SELECT stoc_total, stoc_disponibil FROM carti WHERE carte_id = :id"),
            {'id': carte_id}
        ).fetchone()
        if not book_row:
            return jsonify({'success': False, 'message': 'Cartea nu a fost găsită'}), 404
        
        current_total, current_disponibil = book_row
        new_total = fields.get('stoc_total', current_total)
        new_disponibil = fields.get('stoc_disponibil', current_disponibil)
        
        try:
            new_total = int(new_total)
            new_disponibil = int(new_disponibil)
        except (ValueError, TypeError):
            return jsonify({'success': False, 'message': 'Stocul total și disponibil trebuie să fie numere întregi'}), 400
            
        if new_total < 0 or new_disponibil < 0 or new_disponibil > new_total:
            return jsonify({'success': False, 'message': 'Stocul total/disponibil invalid'}), 400
            
        fields['stoc_total'] = new_total
        fields['stoc_disponibil'] = new_disponibil

    if 'stoc_total' in fields or 'stoc_disponibil' in fields:
        fields['imprumutat'] = fields['stoc_disponibil'] < fields['stoc_total']

    try:
        updated_rows = db.session.query(Carti).filter_by(carte_id=carte_id).update(fields)
        db.session.commit()
        if updated_rows == 0:
            return jsonify({'success': False, 'message': 'Cartea nu a fost găsită'}), 404
    except IntegrityError:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Conflict ISBN'}), 409
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Eroare la actualizarea cărții'}), 500

    return jsonify({'success': True, 'message': 'Carte actualizată cu succes'}), 200

def delete_book(carte_id):
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

def request_book_fizic(user, carte_id):
    book_row = db.session.execute(
        text("SELECT titlu, autor, stoc_disponibil FROM carti WHERE carte_id = :id"),
        {'id': carte_id}
    ).fetchone()

    if not book_row:
        return jsonify({'success': False, 'message': 'Cartea nu a fost găsită'}), 404

    titlu, autor, stoc_disponibil = book_row
    if stoc_disponibil <= 0:
        return jsonify({'success': False, 'message': 'Cartea nu este disponibilă'}), 409

    rows = db.session.execute(
        text("SELECT email FROM users WHERE rol = 'bibliotecar'")
    ).fetchall()
    emailuri_bibliotecari = [r[0] for r in rows if r[0]]

    if not emailuri_bibliotecari:
        logger.warning('Niciun bibliotecar găsit pentru notificarea cererii %d', carte_id)
        return jsonify({'success': False, 'message': 'Niciun bibliotecar disponibil să proceseze cererea'}), 503

    subject = f'Cerere imprumut carte: {titlu}'
    html_body = (
        f'Cerere noua de imprumut\n'
        f'------------------------\n\n'
        f'Utilizator: {user["username"]} ({user["email"]})\n\n'
        f'Carte solicitata:\n'
        f'  Titlu:  {titlu}\n'
        f'  Autor:  {autor}\n'
        f'  ID:     {carte_id}\n\n'
        f'Stoc disponibil: {stoc_disponibil}\n\n'
        f'Intra pe platforma pentru a aproba sau respinge cererea.\n\n'
        f'---\n'
        f'Biblioteca CNI Suceava\n'
        f'Mesaj automat, te rugam nu raspunde la acest email.'
    )

    try:
        db.session.execute(
            text("INSERT INTO cereri_carti (user_id, carte_id, created_at, updated_at) VALUES (:uid, :cid, NOW(), NOW())"),
            {'uid': user['user_id'], 'cid': carte_id}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        logger.exception('Eroare la salvarea cererii în DB')
        return jsonify({'success': False, 'message': 'Eroare la salvarea cererii'}), 500

    send_email(emailuri_bibliotecari, subject, html_body)

    return jsonify({'success': True, 'message': 'Cererea a fost trimisă!'}), 200

def get_book_requests():
    status_filter = request.args.get('status')
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

def update_book_request(cerere_id):
    data = request.get_json(silent=True) or {}
    status_nou = data.get('status')
    if status_nou not in ('approved', 'rejected'):
        return jsonify({'success': False, 'message': 'Status trebuie să fie approved sau rejected'}), 400

    ridicare_de_la_str = (data.get('ridicare_de_la') or '').strip()
    ridicare_pana_la_str = (data.get('ridicare_pana_la') or '').strip()
    if status_nou == 'approved' and (not ridicare_de_la_str or not ridicare_pana_la_str):
        return jsonify({'success': False, 'message': 'ridicare_de_la și ridicare_pana_la sunt obligatorii la aprobare'}), 400

    try:
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

        ridicare_de_la_dt = None
        ridicare_pana_la_dt = None
        
        if status_nou == 'approved':
            try:
                ridicare_de_la_dt  = datetime.datetime.fromisoformat(ridicare_de_la_str)
                ridicare_pana_la_dt = datetime.datetime.fromisoformat(ridicare_pana_la_str)
            except ValueError:
                return jsonify({'success': False, 'message': 'Format dată invalid pentru intervalul de ridicare'}), 400

            db.session.execute(
                text("UPDATE cereri_carti SET status = :status WHERE cerere_id = :id"),
                {'status': status_nou, 'id': cerere_id}
            )
        else:
            db.session.execute(
                text("UPDATE cereri_carti SET status = :status WHERE cerere_id = :id"),
                {'status': status_nou, 'id': cerere_id}
            )

        if status_nou == 'approved' and status_vechi != 'approved':
            interval_de_la   = ridicare_de_la_dt.strftime('%d.%m.%Y %H:%M')
            interval_pana_la = ridicare_pana_la_dt.strftime('%d.%m.%Y %H:%M')
            html_body = (
                f'Salut, {nume_elev}!\n\n'
                f'Cererea ta de imprumut pentru cartea:\n\n'
                f'  Titlu: {titlu}\n'
                f'  Autor: {autor}\n\n'
                f'a fost APROBATA.\n\n'
                f'Poti ridica cartea de la biblioteca in intervalul:\n'
                f'  {interval_de_la} - {interval_pana_la}\n\n'
                f'Daca nu poti ridica cartea in acest interval, te rugam sa contactezi biblioteca.\n\n'
                f'---\n'
                f'Biblioteca CNI Suceava\n'
                f'Mesaj automat, te rugam nu raspunde la acest email.'
            )
            send_email(
                recipients=[email_elev],
                subject=f'Cerere aprobata: {titlu}',
                body=html_body
            )

        db.session.commit()
        return jsonify({'success': True, 'message': f'Cerere {status_nou}'}), 200
    except Exception:
        db.session.rollback()
        logger.exception('Eroare la actualizarea cererii %d', cerere_id)
        return jsonify({'success': False, 'message': 'Eroare la actualizarea cererii'}), 500

def confirma_ridicare(cerere_id):
    try:
        row = db.session.execute(
            text(
                "SELECT cr.user_id, cr.carte_id, cr.status, c.stoc_disponibil "
                "FROM cereri_carti cr "
                "JOIN carti c ON cr.carte_id = c.carte_id "
                "WHERE cr.cerere_id = :id"
            ),
            {'id': cerere_id}
        ).fetchone()

        if not row:
            return jsonify({'success': False, 'message': 'Cererea nu a fost găsită'}), 404

        user_id, carte_id, status_curent, stoc_disponibil = row

        if status_curent != 'approved':
            return jsonify({'success': False, 'message': 'Cererea trebuie să fie aprobată înainte de confirmare'}), 409

        if stoc_disponibil <= 0:
            return jsonify({'success': False, 'message': 'Stoc insuficient — cartea nu mai este disponibilă'}), 409

        now = datetime.datetime.utcnow()
        due = now + datetime.timedelta(days=30)

        db.session.execute(
            text("INSERT INTO imprumuturi_active (user_id, carte_id, data_imprumut, data_scadenta) "
                 "VALUES (:uid, :cid, :now, :due)"),
            {'uid': user_id, 'cid': carte_id, 'now': now, 'due': due}
        )

        db.session.execute(
            text("UPDATE carti SET stoc_disponibil = stoc_disponibil - 1, "
                 "imprumutat = (stoc_disponibil - 1 < stoc_total) "
                 "WHERE carte_id = :cid AND stoc_disponibil > 0"),
            {'cid': carte_id}
        )

        db.session.execute(
            text("UPDATE cereri_carti SET status = 'ridicat' WHERE cerere_id = :id"),
            {'id': cerere_id}
        )

        db.session.commit()
        return jsonify({'success': True, 'message': 'Ridicare confirmată'}), 200
    except Exception:
        db.session.rollback()
        logger.exception('Eroare la confirmarea ridicării pentru cererea %d', cerere_id)
        return jsonify({'success': False, 'message': 'Eroare la confirmarea ridicării'}), 500

def upload_book_image():
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

    query = text("SELECT carte_id FROM carti WHERE carte_id = :carte_id")
    result = db.session.execute(query, {'carte_id': carte_id}).mappings().first()
    if not result:
        return jsonify({'success': False, 'message': 'Cartea nu a fost găsită'}), 404

    ext = file.filename.rsplit('.', 1)[1].lower()

    for imagine_veche in _find_files_by_prefix(BOOK_IMAGES_DIR, str(carte_id)):
        os.remove(os.path.join(BOOK_IMAGES_DIR, imagine_veche))

    filename = f"{carte_id}.{ext}"
    filepath = os.path.join(BOOK_IMAGES_DIR, filename)
    file.save(filepath)

    return jsonify({
        'success': True,
        'message': 'Copertă carte încărcată',
        'filename': filename
    }), 200

def get_book_image(carte_id):
    matches = _find_files_by_prefix(BOOK_IMAGES_DIR, str(carte_id))

    if not matches:
        return jsonify({'success': False, 'message': 'Nicio imagine găsită'}), 404

    return send_from_directory(BOOK_IMAGES_DIR, matches[0])

def upload_book_pdf():
    carte_id = request.form.get('carte_id')
    if not carte_id:
        return jsonify({'success': False, 'message': 'carte_id is required'}), 400
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'Niciun fișier trimis'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'Niciun fișier selectat'}), 400
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'success': False, 'message': 'Doar fișiere PDF sunt acceptate'}), 400

    result = db.session.execute(text("SELECT carte_id FROM carti WHERE carte_id = :id"), {'id': carte_id}).mappings().first()
    if not result:
        return jsonify({'success': False, 'message': 'Cartea nu a fost găsită'}), 404

    os.makedirs(BOOK_PDFS_DIR, exist_ok=True)
    old_path = os.path.join(BOOK_PDFS_DIR, f"{carte_id}.pdf")
    if os.path.exists(old_path):
        os.remove(old_path)

    file.save(os.path.join(BOOK_PDFS_DIR, f"{carte_id}.pdf"))
    return jsonify({'success': True, 'message': 'PDF încărcat'}), 200

def get_book_pdf(carte_id):
    pdf_path = os.path.join(BOOK_PDFS_DIR, f"{carte_id}.pdf")
    if not os.path.exists(pdf_path):
        return jsonify({'success': False, 'message': 'PDF negăsit'}), 404
    return send_from_directory(BOOK_PDFS_DIR, f"{carte_id}.pdf", as_attachment=False)

def delete_book_pdf(carte_id):
    pdf_path = os.path.join(BOOK_PDFS_DIR, f"{carte_id}.pdf")
    if not os.path.exists(pdf_path):
        return jsonify({'success': False, 'message': 'PDF negăsit'}), 404
    os.remove(pdf_path)
    return jsonify({'success': True, 'message': 'PDF șters'}), 200
