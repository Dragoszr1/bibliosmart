from flask import request, jsonify
from sqlalchemy import text
from app.database import db
from app.models import Anunturi
from app.utils.constants import ALLOWED_ANUNT_FIELDS
from app.middlewares.auth import get_current_user
import logging

logger = logging.getLogger(__name__)

def get_anunturi():
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

def create_anunt():
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

def update_anunt(anunt_id):
    data = request.get_json(silent=True) or {}

    fields = {}
    for key in ALLOWED_ANUNT_FIELDS:
        if key in data and data[key] is not None:
            fields[key] = data[key].strip()

    if not fields:
        return jsonify({'success': False, 'message': 'Niciun câmp de actualizat'}), 400

    try:
        updated_rows = db.session.query(Anunturi).filter_by(anunt_id=anunt_id).update(fields)
        db.session.commit()
        if updated_rows == 0:
            return jsonify({'success': False, 'message': 'Anunțul nu a fost găsit'}), 404
        return jsonify({'success': True, 'message': 'Anunț actualizat'}), 200
    except Exception:
        db.session.rollback()
        logger.exception('Eroare la actualizarea anunțului %d', anunt_id)
        return jsonify({'success': False, 'message': 'Eroare la actualizarea anunțului'}), 500

def delete_anunt(anunt_id):
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

def toggle_like_anunt(user, anunt_id):
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
