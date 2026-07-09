import sys

file_path = "backend/app/routes/__init__.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

marker = "# --- CLUB THREADS ---"
idx = content.find(marker)
if idx == -1:
    print("Marker not found!")
    sys.exit(1)

new_content = content[:idx] + marker + """

@main_bp.route('/club/threads', methods=['GET'])
@club_required
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

@main_bp.route('/club/threads', methods=['POST'])
@club_required
def create_club_thread():
    data = request.get_json()
    if not data or not data.get('titlu') or not data.get('continut'):
        return jsonify({'error': 'Titlul și conținutul sunt obligatorii.'}), 400
        
    try:
        is_aprobat = True if request.current_user['rol'] == 'bibliotecar' else False
        new_thread = ClubThreads(
            titlu=data['titlu'],
            continut=data['continut'],
            creat_de=request.current_user['user_id'],
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

@main_bp.route('/club/threads/pending', methods=['GET'])
@bibliotecar_required
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

@main_bp.route('/club/threads/<int:thread_id>/approve', methods=['POST'])
@bibliotecar_required
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

@main_bp.route('/club/threads/<int:thread_id>', methods=['GET'])
@club_required
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

@main_bp.route('/club/threads/<int:thread_id>/comments', methods=['POST'])
@club_required
def add_thread_comment(thread_id):
    data = request.get_json()
    if not data or not data.get('continut'):
        return jsonify({'error': 'Conținutul este obligatoriu.'}), 400
        
    try:
        new_comment = ThreadComments(
            thread_id=thread_id,
            user_id=request.current_user['user_id'],
            continut=data['continut']
        )
        db.session.add(new_comment)
        db.session.commit()
        return jsonify({'message': 'Comentariu adăugat cu succes.', 'comentariu_id': new_comment.comentariu_id}), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Eroare la adăugarea comentariului: {e}")
        return jsonify({'error': 'A apărut o eroare la adăugarea comentariului.'}), 500

@main_bp.route('/club/threads/comments/<int:comentariu_id>/subcomments', methods=['POST'])
@club_required
def add_thread_subcomment(comentariu_id):
    data = request.get_json()
    if not data or not data.get('continut'):
        return jsonify({'error': 'Conținutul este obligatoriu.'}), 400
        
    try:
        new_subcomment = ThreadSubcomments(
            comentariu_id=comentariu_id,
            user_id=request.current_user['user_id'],
            continut=data['continut']
        )
        db.session.add(new_subcomment)
        db.session.commit()
        return jsonify({'message': 'Subcomentariu adăugat cu succes.', 'subcomentariu_id': new_subcomment.subcomentariu_id}), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Eroare la adăugarea subcomentariului: {e}")
        return jsonify({'error': 'A apărut o eroare la adăugarea subcomentariului.'}), 500

@main_bp.route('/club/threads/comments/<int:comentariu_id>/like', methods=['POST'])
@club_required
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

@main_bp.route('/club/threads/subcomments/<int:subcomentariu_id>/like', methods=['POST'])
@club_required
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

@main_bp.route('/club/threads/<int:thread_id>', methods=['DELETE'])
@club_required
def delete_club_thread(thread_id):
    try:
        thread = db.session.query(ClubThreads).filter_by(thread_id=thread_id).first()
        if not thread:
            return jsonify({'error': 'Thread-ul nu a fost găsit.'}), 404
            
        if request.current_user['rol'] != 'bibliotecar':
            return jsonify({'error': 'Nu aveți permisiunea de a șterge.'}), 403
            
        db.session.delete(thread)
        db.session.commit()
        return jsonify({'message': 'Thread șters cu succes.'}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Eroare la ștergerea thread-ului: {e}")
        return jsonify({'error': 'A apărut o eroare la ștergerea thread-ului.'}), 500

@main_bp.route('/club/threads/comments/<int:comentariu_id>', methods=['DELETE'])
@club_required
def delete_thread_comment(comentariu_id):
    try:
        comment = db.session.query(ThreadComments).filter_by(comentariu_id=comentariu_id).first()
        if not comment:
            return jsonify({'error': 'Comentariul nu a fost găsit.'}), 404
            
        if request.current_user['rol'] != 'bibliotecar':
            return jsonify({'error': 'Nu aveți permisiunea de a șterge.'}), 403
            
        db.session.delete(comment)
        db.session.commit()
        return jsonify({'message': 'Comentariu șters cu succes.'}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Eroare la ștergerea comentariului: {e}")
        return jsonify({'error': 'A apărut o eroare la ștergerea comentariului.'}), 500

@main_bp.route('/club/threads/subcomments/<int:subcomentariu_id>', methods=['DELETE'])
@club_required
def delete_thread_subcomment(subcomentariu_id):
    try:
        subcomment = db.session.query(ThreadSubcomments).filter_by(subcomentariu_id=subcomentariu_id).first()
        if not subcomment:
            return jsonify({'error': 'Subcomentariul nu a fost găsit.'}), 404
            
        if request.current_user['rol'] != 'bibliotecar':
            return jsonify({'error': 'Nu aveți permisiunea de a șterge.'}), 403
            
        db.session.delete(subcomment)
        db.session.commit()
        return jsonify({'message': 'Subcomentariu șters cu succes.'}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Eroare la ștergerea subcomentariului: {e}")
        return jsonify({'error': 'A apărut o eroare la ștergerea subcomentariului.'}), 500
"""

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Rewrote routes successfully.")
