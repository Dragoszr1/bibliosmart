from flask import request, jsonify
from sqlalchemy import text
from app.database import db
import logging

logger = logging.getLogger(__name__)

def get_reviews():
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

def submit_review(user):
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

    book = db.session.execute(text("SELECT carte_id FROM carti WHERE carte_id = :id"), {'id': carte_id}).fetchone()
    if not book:
        return jsonify({'success': False, 'message': 'Cartea nu a fost găsită'}), 404

    try:
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

def get_user_reviews(user):
    user_id = user['user_id']

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
