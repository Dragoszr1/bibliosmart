from flask import request, jsonify, send_from_directory
from sqlalchemy import text
from app.database import db
from app.models import Users, ClubThreads, ThreadComments, ThreadSubcomments
from app.utils.constants import CLUB_ANNOUNCEMENT_IMAGES_DIR
from app.utils.file_utils import allowed_file, _find_files_by_prefix, _save_club_activity_image
from app.utils.validators import _get_request_data
import datetime
import secrets
import os
import logging

logger = logging.getLogger(__name__)

MAX_INVITE_HOURS = 168
SAPTAMANI_VALIDE = {'anterioara', 'curenta', 'urmatoare'}
TIPURI_VALIDE    = {'anunt', 'sarcina', 'activitate'}

def create_club_invite(user):
    data = request.get_json(silent=True) or {}
    try:
        expires_in_hours = int(data.get('expires_in_hours', 24))
    except (ValueError, TypeError):
        expires_in_hours = 24

    expires_in_hours = max(1, min(expires_in_hours, MAX_INVITE_HOURS))

    token = secrets.token_urlsafe(32)
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(hours=expires_in_hours)

    try:
        db.session.execute(
            text("INSERT INTO club_invites (token, created_by, expires_at) VALUES (:token, :uid, :exp)"),
            {'token': token, 'uid': user['user_id'], 'exp': expires_at}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        logger.exception('Eroare la crearea invitației de club')
        return jsonify({'success': False, 'message': 'Eroare la generarea link-ului'}), 500

    return jsonify({
        'success': True,
        'token': token,
        'expires_at': expires_at.strftime('%d.%m.%Y %H:%M'),
        'expires_in_hours': expires_in_hours
    }), 201

def join_club(user, token):
    try:
        row = db.session.execute(
            text("SELECT expires_at FROM club_invites WHERE token = :token"),
            {'token': token}
        ).fetchone()

        if not row:
            return jsonify({'success': False, 'message': 'Link de invitație invalid'}), 404

        if datetime.datetime.utcnow() > row[0]:
            return jsonify({'success': False, 'message': 'Link-ul de invitație a expirat'}), 410

        member_row = db.session.execute(
            text("SELECT club FROM users WHERE user_id = :uid"),
            {'uid': user['user_id']}
        ).fetchone()

        if member_row and member_row[0]:
            return jsonify({'success': True, 'already_member': True, 'message': 'Ești deja membru al clubului'}), 200

        db.session.execute(
            text("UPDATE users SET club = 1 WHERE user_id = :uid"),
            {'uid': user['user_id']}
        )
        db.session.commit()
        return jsonify({'success': True, 'already_member': False, 'message': 'Bun venit în Clubul de Literatură!'}), 200
    except Exception:
        db.session.rollback()
        logger.exception('Eroare la join club pentru token %s', token)
        return jsonify({'success': False, 'message': 'Eroare la procesarea invitației'}), 500

def get_activitati():
    saptamana = request.args.get('saptamana', 'curenta')
    if saptamana not in SAPTAMANI_VALIDE:
        saptamana = 'curenta'
    try:
        rows = db.session.execute(
            text("""
                SELECT a.activitate_id, a.titlu, a.continut, a.tip, a.saptamana,
                       a.creat_la, a.actualizat_la, a.nume_imagine,
                       u.username, u.rol,
                       (SELECT COUNT(*) FROM comentarii_activitati c WHERE c.activitate_id = a.activitate_id) AS nr_comentarii
                FROM activitati_club a
                JOIN users u ON u.user_id = a.creat_de
                WHERE a.saptamana = :s
                ORDER BY a.creat_la DESC
            """),
            {'s': saptamana}
        ).fetchall()
        activitati = []
        for r in rows:
            activitati.append({
                'activitate_id': r[0],
                'titlu': r[1],
                'continut': r[2],
                'tip': r[3],
                'saptamana': r[4],
                'creat_la': r[5].strftime('%d.%m.%Y %H:%M') if r[5] else None,
                'actualizat_la': r[6].strftime('%d.%m.%Y %H:%M') if r[6] else None,
                'imagine_url': f'/api/club/activitati/{r[0]}/imagine' if r[7] else None,
                'autor': r[8],
                'autor_rol': r[9],
                'nr_comentarii': r[10]
            })
        return jsonify({'success': True, 'activitati': activitati}), 200
    except Exception:
        logger.exception('Eroare la get activitati club')
        return jsonify({'success': False, 'message': 'Eroare la încărcarea activităților'}), 500

def create_activitate(user):
    data = _get_request_data()
    titlu    = (data.get('titlu') or '').strip()
    continut = (data.get('continut') or '').strip()
    tip      = data.get('tip', 'activitate')
    saptamana = data.get('saptamana', 'curenta')
    image_file = request.files.get('image')

    if not titlu:
        return jsonify({'success': False, 'message': 'Titlul este obligatoriu'}), 400
    if tip not in TIPURI_VALIDE:
        tip = 'activitate'
    if saptamana not in SAPTAMANI_VALIDE:
        saptamana = 'curenta'
    if image_file and not allowed_file(image_file.filename):
        return jsonify({'success': False, 'message': 'Format imagine nepermis. Folosește png, jpg, jpeg, gif sau webp.'}), 400

    try:
        result = db.session.execute(
            text("""INSERT INTO activitati_club (titlu, continut, tip, saptamana, creat_de)
                    VALUES (:titlu, :continut, :tip, :s, :uid)"""),
            {'titlu': titlu, 'continut': continut or None, 'tip': tip,
             's': saptamana, 'uid': user['user_id']}
        )
        activitate_id = result.lastrowid
        if image_file and tip == 'anunt':
            filename = _save_club_activity_image(image_file, activitate_id)
            if filename:
                db.session.execute(
                    text("UPDATE activitati_club SET nume_imagine = :img WHERE activitate_id = :id"),
                    {'img': filename, 'id': activitate_id}
                )
        db.session.commit()
        return jsonify({'success': True, 'activitate_id': activitate_id}), 201
    except Exception:
        db.session.rollback()
        logger.exception('Eroare la creare activitate club')
        return jsonify({'success': False, 'message': 'Eroare la salvarea activității'}), 500

def get_activitate_image(activitate_id):
    matches = _find_files_by_prefix(CLUB_ANNOUNCEMENT_IMAGES_DIR, str(activitate_id))
    if not matches:
        return jsonify({'success': False, 'message': 'Imaginea nu a fost găsită'}), 404
    return send_from_directory(CLUB_ANNOUNCEMENT_IMAGES_DIR, matches[0])

def delete_activitate(activitate_id):
    try:
        for old in _find_files_by_prefix(CLUB_ANNOUNCEMENT_IMAGES_DIR, str(activitate_id)):
            try:
                os.remove(os.path.join(CLUB_ANNOUNCEMENT_IMAGES_DIR, old))
            except OSError:
                pass
        db.session.execute(
            text("DELETE FROM activitati_club WHERE activitate_id = :id"),
            {'id': activitate_id}
        )
        db.session.commit()
        return jsonify({'success': True}), 200
    except Exception:
        db.session.rollback()
        logger.exception('Eroare la ștergere activitate %s', activitate_id)
        return jsonify({'success': False, 'message': 'Eroare la ștergere'}), 500

def get_comentarii(activitate_id):
    try:
        rows = db.session.execute(
            text("""
                SELECT c.comentariu_id, c.continut, c.creat_la,
                       u.username, u.rol, u.user_id
                FROM comentarii_activitati c
                JOIN users u ON u.user_id = c.user_id
                WHERE c.activitate_id = :id
                ORDER BY c.creat_la ASC
            """),
            {'id': activitate_id}
        ).fetchall()
        comentarii = [{
            'comentariu_id': r[0],
            'continut': r[1],
            'creat_la': r[2].strftime('%d.%m.%Y %H:%M') if r[2] else None,
            'autor': r[3],
            'autor_rol': r[4],
            'user_id': r[5]
        } for r in rows]
        return jsonify({'success': True, 'comentarii': comentarii}), 200
    except Exception:
        logger.exception('Eroare la get comentarii activitate %s', activitate_id)
        return jsonify({'success': False, 'message': 'Eroare la încărcarea comentariilor'}), 500

def post_comentariu(user, activitate_id):
    data = request.get_json(silent=True) or {}
    continut = (data.get('continut') or '').strip()
    if not continut:
        return jsonify({'success': False, 'message': 'Comentariul nu poate fi gol'}), 400
    if len(continut) > 2000:
        return jsonify({'success': False, 'message': 'Comentariul este prea lung (max 2000 caractere)'}), 400

    exists = db.session.execute(
        text("SELECT 1 FROM activitati_club WHERE activitate_id = :id"),
        {'id': activitate_id}
    ).fetchone()
    if not exists:
        return jsonify({'success': False, 'message': 'Activitatea nu există'}), 404

    try:
        result = db.session.execute(
            text("INSERT INTO comentarii_activitati (activitate_id, user_id, continut) VALUES (:aid, :uid, :c)"),
            {'aid': activitate_id, 'uid': user['user_id'], 'c': continut}
        )
        db.session.commit()
        return jsonify({'success': True, 'comentariu_id': result.lastrowid}), 201
    except Exception:
        db.session.rollback()
        logger.exception('Eroare la post comentariu activitate %s', activitate_id)
        return jsonify({'success': False, 'message': 'Eroare la salvarea comentariului'}), 500

def delete_comentariu(user, activitate_id, comentariu_id):
    row = db.session.execute(
        text("SELECT user_id FROM comentarii_activitati WHERE comentariu_id = :cid AND activitate_id = :aid"),
        {'cid': comentariu_id, 'aid': activitate_id}
    ).fetchone()
    if not row:
        return jsonify({'success': False, 'message': 'Comentariul nu există'}), 404
    if row[0] != user['user_id'] and user.get('rol') != 'bibliotecar':
        return jsonify({'success': False, 'message': 'Nu poți șterge comentariul altcuiva'}), 403
    try:
        db.session.execute(
            text("DELETE FROM comentarii_activitati WHERE comentariu_id = :cid"),
            {'cid': comentariu_id}
        )
        db.session.commit()
        return jsonify({'success': True}), 200
    except Exception:
        db.session.rollback()
        logger.exception('Eroare la ștergere comentariu %s', comentariu_id)
        return jsonify({'success': False, 'message': 'Eroare la ștergere'}), 500

def get_club_threads():
    try:
        threads = db.session.query(
            ClubThreads.thread_id,
            ClubThreads.titlu,
            ClubThreads.continut,
            ClubThreads.creat_la,
            Users.username,
            Users.user_id.label('autor_id')
        ).join(Users, ClubThreads.creat_de == Users.user_id).filter(ClubThreads.aprobat == True).order_by(ClubThreads.creat_la.desc()).all()
        
        result = []
        for t in threads:
            result.append({
                'thread_id': t.thread_id,
                'titlu': t.titlu,
                'continut': t.continut,
                'creat_la': t.creat_la.isoformat() if t.creat_la else None,
                'autor': t.username,
                'autor_id': t.autor_id
            })
        return jsonify({'threads': result}), 200
    except Exception as e:
        logger.error(f"Eroare la preluarea thread-urilor: {e}")
        return jsonify({'error': 'A apărut o eroare la preluarea thread-urilor.'}), 500

def create_club_thread(user):
    data = request.get_json()
    if not data or not data.get('titlu') or not data.get('continut'):
        return jsonify({'error': 'Titlul și conținutul sunt obligatorii.'}), 400
        
    try:
        is_aprobat = True if user['rol'] == 'bibliotecar' else False
        new_thread = ClubThreads(
            titlu=data['titlu'],
            continut=data['continut'],
            creat_de=user['user_id'],
            aprobat=is_aprobat
        )
        db.session.add(new_thread)
        db.session.commit()
        msg = 'Discuția a fost creată și este publică.' if is_aprobat else 'Discuția ta a fost trimisă spre moderare.'
        return jsonify({'message': msg, 'thread_id': new_thread.thread_id, 'aprobat': is_aprobat}), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Eroare la crearea thread-ului: {e}")
        return jsonify({'error': 'A apărut o eroare la crearea thread-ului.'}), 500

def get_pending_threads():
    try:
        threads = db.session.query(
            ClubThreads.thread_id,
            ClubThreads.titlu,
            ClubThreads.continut,
            ClubThreads.creat_la,
            Users.username,
            Users.user_id.label('autor_id')
        ).join(Users, ClubThreads.creat_de == Users.user_id).filter(ClubThreads.aprobat == False).order_by(ClubThreads.creat_la.desc()).all()
        
        result = []
        for t in threads:
            result.append({
                'thread_id': t.thread_id,
                'titlu': t.titlu,
                'continut': t.continut,
                'creat_la': t.creat_la.isoformat() if t.creat_la else None,
                'autor': t.username,
                'autor_id': t.autor_id
            })
        return jsonify({'threads': result}), 200
    except Exception as e:
        logger.error(f"Eroare la preluarea discuțiilor în așteptare: {e}")
        return jsonify({'error': 'A apărut o eroare la preluarea discuțiilor în așteptare.'}), 500

def approve_club_thread(thread_id):
    try:
        thread = db.session.query(ClubThreads).filter_by(thread_id=thread_id).first()
        if not thread:
            return jsonify({'error': 'Discuția nu a fost găsită.'}), 404
            
        thread.aprobat = True
        db.session.commit()
        return jsonify({'message': 'Discuție aprobată cu succes.'}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Eroare la aprobarea discuției: {e}")
        return jsonify({'error': 'A apărut o eroare la aprobarea discuției.'}), 500

def get_club_thread(thread_id):
    try:
        thread = db.session.query(
            ClubThreads.thread_id,
            ClubThreads.titlu,
            ClubThreads.continut,
            ClubThreads.creat_la,
            Users.username,
            Users.user_id.label('autor_id')
        ).join(Users, ClubThreads.creat_de == Users.user_id).filter(ClubThreads.thread_id == thread_id).first()
        
        if not thread:
            return jsonify({'error': 'Thread-ul nu a fost găsit.'}), 404
            
        comments_query = db.session.query(
            ThreadComments.comentariu_id,
            ThreadComments.continut,
            ThreadComments.likes,
            ThreadComments.creat_la,
            Users.username,
            Users.user_id.label('autor_id')
        ).join(Users, ThreadComments.user_id == Users.user_id).filter(ThreadComments.thread_id == thread_id).order_by(ThreadComments.creat_la.asc()).all()
        
        comments = []
        for c in comments_query:
            subcomments_query = db.session.query(
                ThreadSubcomments.subcomentariu_id,
                ThreadSubcomments.continut,
                ThreadSubcomments.likes,
                ThreadSubcomments.creat_la,
                Users.username,
                Users.user_id.label('autor_id')
            ).join(Users, ThreadSubcomments.user_id == Users.user_id).filter(ThreadSubcomments.comentariu_id == c.comentariu_id).order_by(ThreadSubcomments.creat_la.asc()).all()
            
            subcomments = []
            for sc in subcomments_query:
                subcomments.append({
                    'subcomentariu_id': sc.subcomentariu_id,
                    'continut': sc.continut,
                    'likes': sc.likes,
                    'creat_la': sc.creat_la.isoformat() if sc.creat_la else None,
                    'autor': sc.username,
                    'autor_id': sc.autor_id
                })
                
            comments.append({
                'comentariu_id': c.comentariu_id,
                'continut': c.continut,
                'likes': c.likes,
                'creat_la': c.creat_la.isoformat() if c.creat_la else None,
                'autor': c.username,
                'autor_id': c.autor_id,
                'subcomments': subcomments
            })
            
        return jsonify({
            'thread': {
                'thread_id': thread.thread_id,
                'titlu': thread.titlu,
                'continut': thread.continut,
                'creat_la': thread.creat_la.isoformat() if thread.creat_la else None,
                'autor': thread.username,
                'autor_id': thread.autor_id,
                'comments': comments
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Eroare la preluarea thread-ului: {e}")
        return jsonify({'error': 'A apărut o eroare la preluarea thread-ului.'}), 500

def add_thread_comment(user, thread_id):
    data = request.get_json()
    if not data or not data.get('continut'):
        return jsonify({'error': 'Conținutul este obligatoriu.'}), 400
        
    try:
        new_comment = ThreadComments(
            thread_id=thread_id,
            user_id=user['user_id'],
            continut=data['continut']
        )
        db.session.add(new_comment)
        db.session.commit()
        return jsonify({'message': 'Comentariu adăugat cu succes.', 'comentariu_id': new_comment.comentariu_id}), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Eroare la adăugarea comentariului: {e}")
        return jsonify({'error': 'A apărut o eroare la adăugarea comentariului.'}), 500

def add_thread_subcomment(user, comentariu_id):
    data = request.get_json()
    if not data or not data.get('continut'):
        return jsonify({'error': 'Conținutul este obligatoriu.'}), 400
        
    try:
        new_subcomment = ThreadSubcomments(
            comentariu_id=comentariu_id,
            user_id=user['user_id'],
            continut=data['continut']
        )
        db.session.add(new_subcomment)
        db.session.commit()
        return jsonify({'message': 'Subcomentariu adăugat cu succes.', 'subcomentariu_id': new_subcomment.subcomentariu_id}), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Eroare la adăugarea subcomentariului: {e}")
        return jsonify({'error': 'A apărut o eroare la adăugarea subcomentariului.'}), 500

def like_thread_comment(comentariu_id):
    try:
        comment = db.session.query(ThreadComments).filter_by(comentariu_id=comentariu_id).first()
        if not comment:
            return jsonify({'error': 'Comentariul nu a fost găsit.'}), 404
            
        comment.likes += 1
        db.session.commit()
        return jsonify({'message': 'Comentariu apreciat cu succes.', 'likes': comment.likes}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Eroare la aprecierea comentariului: {e}")
        return jsonify({'error': 'A apărut o eroare la aprecierea comentariului.'}), 500

def like_thread_subcomment(subcomentariu_id):
    try:
        subcomment = db.session.query(ThreadSubcomments).filter_by(subcomentariu_id=subcomentariu_id).first()
        if not subcomment:
            return jsonify({'error': 'Subcomentariul nu a fost găsit.'}), 404
            
        subcomment.likes += 1
        db.session.commit()
        return jsonify({'message': 'Subcomentariu apreciat cu succes.', 'likes': subcomment.likes}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Eroare la aprecierea subcomentariului: {e}")
        return jsonify({'error': 'A apărut o eroare la aprecierea subcomentariului.'}), 500

def delete_club_thread(user, thread_id):
    try:
        thread = db.session.query(ClubThreads).filter_by(thread_id=thread_id).first()
        if not thread:
            return jsonify({'error': 'Thread-ul nu a fost găsit.'}), 404
            
        if user['rol'] != 'bibliotecar':
            return jsonify({'error': 'Nu aveți permisiunea de a șterge.'}), 403
            
        db.session.delete(thread)
        db.session.commit()
        return jsonify({'message': 'Thread șters cu succes.'}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Eroare la ștergerea thread-ului: {e}")
        return jsonify({'error': 'A apărut o eroare la ștergerea thread-ului.'}), 500

def delete_thread_comment(user, comentariu_id):
    try:
        comment = db.session.query(ThreadComments).filter_by(comentariu_id=comentariu_id).first()
        if not comment:
            return jsonify({'error': 'Comentariul nu a fost găsit.'}), 404
            
        if user['rol'] != 'bibliotecar':
            return jsonify({'error': 'Nu aveți permisiunea de a șterge.'}), 403
            
        db.session.delete(comment)
        db.session.commit()
        return jsonify({'message': 'Comentariu șters cu succes.'}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Eroare la ștergerea comentariului: {e}")
        return jsonify({'error': 'A apărut o eroare la ștergerea comentariului.'}), 500

def delete_thread_subcomment(user, subcomentariu_id):
    try:
        subcomment = db.session.query(ThreadSubcomments).filter_by(subcomentariu_id=subcomentariu_id).first()
        if not subcomment:
            return jsonify({'error': 'Subcomentariul nu a fost găsit.'}), 404
            
        if user['rol'] != 'bibliotecar':
            return jsonify({'error': 'Nu aveți permisiunea de a șterge.'}), 403
            
        db.session.delete(subcomment)
        db.session.commit()
        return jsonify({'message': 'Subcomentariu șters cu succes.'}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Eroare la ștergerea subcomentariului: {e}")
        return jsonify({'error': 'A apărut o eroare la ștergerea subcomentariului.'}), 500
