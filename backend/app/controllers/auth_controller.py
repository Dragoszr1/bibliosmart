from flask import request, jsonify, send_from_directory
from sqlalchemy import text
from app.database import db
from app.utils.validators import normalize_cni_email, normalize_role
from app.utils.email_utils import send_email
from app.utils.auth import create_jwt_token, set_jwt_cookie, clear_jwt_cookie
from app.utils.constants import USERNAME_REGEX, PROFILE_PICTURES_DIR
from app.utils.file_utils import allowed_file, _find_files_by_prefix
import bcrypt
import random
import secrets
import datetime
import os
from sqlalchemy.exc import IntegrityError

def login():
    data = request.get_json(silent=True) or {}
    raw_email = data.get('email')
    parola = data.get('password')

    if not raw_email or not parola:
        return jsonify({'success': False, 'message': 'Email și parola sunt obligatorii'}), 400

    email = normalize_cni_email(raw_email)
    if not email:
        return jsonify({'success': False, 'message': 'Doar emailurile @cni-sv.ro sunt permise'}), 400

    result = db.session.execute(
        text("SELECT user_id, username, email, hashed_password, rol FROM users WHERE email = :email"),
        {'email': email}
    ).mappings().first()

    if not result:
        return jsonify({'success': False, 'message': 'Credențiale invalide'}), 401

    parola_hash = result.get('hashed_password')
    if not parola_hash or not bcrypt.checkpw(parola.encode('utf-8'), parola_hash.encode('utf-8')):
        return jsonify({'success': False, 'message': 'Credențiale invalide'}), 401

    db.session.execute(
        text("DELETE FROM coduri_verificare WHERE user_id = :uid"),
        {'uid': result['user_id']}
    )

    code = f"{random.randint(0, 999999):06d}"
    temp_token = secrets.token_urlsafe(32)
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)

    db.session.execute(
        text("INSERT INTO coduri_verificare (user_id, code, temp_token, expires_at) VALUES (:uid, :code, :token, :exp)"),
        {'uid': result['user_id'], 'code': code, 'token': temp_token, 'exp': expires_at}
    )
    db.session.commit()

    body = (
        f'Salut, {result["username"]}!\n\n'
        f'Codul tau de verificare pentru autentificarea in Biblioteca CNI este:\n\n'
        f'    {code}\n\n'
        f'Codul este valabil 10 minute. Nu il impartasi cu nimeni.\n\n'
        f'Daca nu ai incercat sa te autentifici, ignora acest mesaj.\n\n'
        f'---\n'
        f'Biblioteca CNI Suceava\n'
        f'Mesaj automat, te rugam nu raspunde la acest email.'
    )
    send_email([result['email']], 'Cod de verificare - Biblioteca CNI', body)

    return jsonify({'success': True, 'step': 'verify', 'temp_token': temp_token}), 200

def verify_code():
    data = request.get_json(silent=True) or {}
    temp_token = (data.get('temp_token') or '').strip()
    code = (data.get('code') or '').strip()

    if not temp_token or not code:
        return jsonify({'success': False, 'message': 'Token și cod sunt obligatorii'}), 400

    row = db.session.execute(
        text("SELECT vc.id, vc.user_id, vc.code, vc.expires_at, u.username, u.email, u.rol "
             "FROM coduri_verificare vc "
             "JOIN users u ON u.user_id = vc.user_id "
             "WHERE vc.temp_token = :token"),
        {'token': temp_token}
    ).mappings().first()

    if not row:
        return jsonify({'success': False, 'message': 'Sesiune de verificare invalidă'}), 401

    if datetime.datetime.utcnow() > row['expires_at']:
        db.session.execute(text("DELETE FROM coduri_verificare WHERE id = :id"), {'id': row['id']})
        db.session.commit()
        return jsonify({'success': False, 'message': 'Codul a expirat. Încearcă să te autentifici din nou.'}), 401

    if code != row['code']:
        db.session.execute(text("DELETE FROM coduri_verificare WHERE id = :id"), {'id': row['id']})
        db.session.commit()
        return jsonify({'success': False, 'message': 'Cod incorect. Sesiunea de verificare a fost anulată. Te rugăm să încerci din nou.'}), 401

    db.session.execute(text("DELETE FROM coduri_verificare WHERE id = :id"), {'id': row['id']})
    db.session.commit()

    token = create_jwt_token(user_id=row['user_id'], username=row['username'], email=row['email'])
    resp = jsonify({
        'success': True,
        'message': 'Autentificare reușită',
        'user': {
            'user_id': row['user_id'],
            'username': row['username'],
            'email': row['email'],
            'rol': normalize_role(row['rol'])
        }
    })
    set_jwt_cookie(resp, token)
    return resp, 200

def auth_me(user):
    row = db.session.execute(
        text("SELECT club FROM users WHERE user_id = :uid"),
        {'uid': user['user_id']}
    ).fetchone()
    return jsonify({
        'success': True,
        'user_id': user['user_id'],
        'username': user['username'],
        'email': user['email'],
        'rol': user['rol'],
        'club': bool(row[0]) if row else False
    }), 200

def logout():
    resp = jsonify({'success': True, 'message': 'Deconectat cu succes'})
    clear_jwt_cookie(resp)
    return resp, 200

def forgot_password():
    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip().lower()

    if not email:
        return jsonify({'success': False, 'message': 'Email-ul este obligatoriu'}), 400

    row = db.session.execute(
        text("SELECT user_id, username FROM users WHERE email = :email"),
        {'email': email}
    ).fetchone()

    if not row:
        return jsonify({'success': True, 'message': 'Dacă email-ul există, s-a trimis un link de resetare.'}), 200

    user_id = row[0]
    username = row[1]
    token = secrets.token_urlsafe(32)
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

    try:
        db.session.execute(
            text("INSERT INTO password_reset_tokens (token, user_id, expires_at) VALUES (:token, :uid, :exp)"),
            {'token': token, 'uid': user_id, 'exp': expires_at}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Eroare la generarea token-ului.'}), 500

    frontend_url = request.headers.get('Origin')
    if not frontend_url:
        referer = request.headers.get('Referer')
        if referer:
            from urllib.parse import urlparse
            parsed_referer = urlparse(referer)
            frontend_url = f"{parsed_referer.scheme}://{parsed_referer.netloc}"
        else:
            frontend_url = "http://localhost:5173"

    reset_url = f"{frontend_url}/reset-password/{token}"
    
    html_body = (
        f"Salut {username},\n\n"
        f"Am primit o cerere de resetare a parolei pentru contul tău.\n"
        f"Accesează acest link pentru a o reseta:\n"
        f"{reset_url}\n\n"
        f"Acest link este valabil o oră. Dacă nu ai cerut asta, ignoră acest email.\n\n"
        f"Echipa Biblioteca"
    )

    send_email([email], "Resetare Parolă", html_body)
    return jsonify({'success': True, 'message': 'Dacă email-ul există, s-a trimis un link de resetare.'}), 200

def reset_password(token):
    data = request.get_json(silent=True) or {}
    new_password = data.get('password')

    if not new_password or len(new_password) < 6:
        return jsonify({'success': False, 'message': 'Parola trebuie să aibă minim 6 caractere'}), 400

    now = datetime.datetime.utcnow()

    row = db.session.execute(
        text("SELECT user_id, expires_at FROM password_reset_tokens WHERE token = :token"),
        {'token': token}
    ).fetchone()

    if not row:
        return jsonify({'success': False, 'message': 'Token invalid sau expirat.'}), 400
        
    user_id = row[0]
    expires_at = row[1]

    if expires_at < now:
        db.session.execute(text("DELETE FROM password_reset_tokens WHERE token = :token"), {'token': token})
        db.session.commit()
        return jsonify({'success': False, 'message': 'Token expirat.'}), 400

    hashed_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        db.session.execute(
            text("UPDATE users SET hashed_password = :hpw WHERE user_id = :uid"),
            {'hpw': hashed_pw, 'uid': user_id}
        )
        db.session.execute(
            text("DELETE FROM password_reset_tokens WHERE token = :token"),
            {'token': token}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Eroare la resetarea parolei.'}), 500

    return jsonify({'success': True, 'message': 'Parola a fost resetată cu succes!'}), 200

def profile(user):
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

def books_read(user):
    query = text(
        "SELECT c.carte_id, c.titlu, c.autor, c.ISBN "
        "FROM carti_citite cc "
        "JOIN carti c ON cc.carte_id = c.carte_id "
        "WHERE cc.user_id = :user_id"
    )
    rows = db.session.execute(query, {'user_id': user['user_id']}).mappings().all()

    books = []
    for row in rows:
        books.append({
            'carte_id': row.get('carte_id'),
            'titlu': row.get('titlu'),
            'autor': row.get('autor'),
            'ISBN': row.get('ISBN')
        })

    return jsonify({'success': True, 'books': books}), 200

def update_profile(user):
    data = request.get_json(silent=True) or {}
    description = data.get('description')

    if description is not None:
        description = str(description).strip()
        if len(description) > 255:
            return jsonify({'success': False, 'message': 'Descrierea este prea lungă (max 255 caractere)'}), 400

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

def register():
    data = request.get_json(silent=True) or {}
    username = data.get('user') or data.get('username') or data.get('fullName')
    raw_email = data.get('email')
    parola = data.get('password')

    if not username or not raw_email or not parola:
        return jsonify({'success': False, 'message': 'Username, email și parola sunt obligatorii'}), 400

    username = username.strip()
    if not USERNAME_REGEX.match(username):
        return jsonify({'success': False, 'message': 'Numele complet trebuie să aibă între 3 și 50 de caractere și să conțină doar litere, cifre, spații, puncte, cratime sau caractere de subliniere'}), 400

    email = normalize_cni_email(raw_email)
    if not email:
        return jsonify({'success': False, 'message': 'Doar emailurile @cni-sv.ro sunt permise'}), 400

    if len(parola) < 8 or len(parola) > 128:
        return jsonify({'success': False, 'message': 'Parola trebuie să aibă între 8 și 128 de caractere'}), 400

    parola_hash = bcrypt.hashpw(parola.encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8')
    values = {
        'username': username,
        'email': email,
        'hashed_password': parola_hash,
        'rol': 'user',
        'telefon': None,
        'club': 0
    }

    insert_query = text(
        "INSERT INTO users (username, email, hashed_password, rol, telefon, club) VALUES (:username, :email, :hashed_password, :rol, :telefon, :club)"
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

    return jsonify({'success': True, 'message': 'Cont creat cu succes. Te poti autentifica acum.'}), 201

def upload_profile_picture(user):
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'Niciun fișier trimis'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'Niciun fișier selectat'}), 400

    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'Tip de fișier nepermis. Folosește png, jpg, jpeg, gif sau webp'}), 400

    username = user['username']
    ext = file.filename.rsplit('.', 1)[1].lower()

    for poza_veche in _find_files_by_prefix(PROFILE_PICTURES_DIR, username):
        os.remove(os.path.join(PROFILE_PICTURES_DIR, poza_veche))

    filename = f"{username}.{ext}"
    filepath = os.path.join(PROFILE_PICTURES_DIR, filename)
    file.save(filepath)

    return jsonify({
        'success': True,
        'message': 'Poză de profil încărcată',
        'filename': filename
    }), 200

def get_profile_picture(username):
    matches = _find_files_by_prefix(PROFILE_PICTURES_DIR, username)

    if not matches:
        return send_from_directory(PROFILE_PICTURES_DIR, 'default.jpg')

    return send_from_directory(PROFILE_PICTURES_DIR, matches[0])
