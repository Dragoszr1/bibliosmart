from flask import Blueprint, request
from app.middlewares.auth import jwt_required, bibliotecar_required, club_required
from app.controllers import club_controller

club_bp = Blueprint('club', __name__)

@club_bp.route('/invite', methods=['POST'])
@bibliotecar_required
def create_club_invite():
    return club_controller.create_club_invite(request.current_user)

@club_bp.route('/join/<token>', methods=['POST'])
@jwt_required
def join_club(token):
    return club_controller.join_club(request.current_user, token)

@club_bp.route('/activitati', methods=['GET'])
@club_required
def get_activitati():
    return club_controller.get_activitati()

@club_bp.route('/activitati', methods=['POST'])
@bibliotecar_required
def create_activitate():
    return club_controller.create_activitate(request.current_user)

@club_bp.route('/activitati/<int:activitate_id>/imagine', methods=['GET'])
def get_activitate_image(activitate_id):
    return club_controller.get_activitate_image(activitate_id)

@club_bp.route('/activitati/<int:activitate_id>', methods=['DELETE'])
@bibliotecar_required
def delete_activitate(activitate_id):
    return club_controller.delete_activitate(activitate_id)

@club_bp.route('/activitati/<int:activitate_id>/comentarii', methods=['GET'])
@club_required
def get_comentarii(activitate_id):
    return club_controller.get_comentarii(activitate_id)

@club_bp.route('/activitati/<int:activitate_id>/comentarii', methods=['POST'])
@club_required
def post_comentariu(activitate_id):
    return club_controller.post_comentariu(request.current_user, activitate_id)

@club_bp.route('/activitati/<int:activitate_id>/comentarii/<int:comentariu_id>', methods=['DELETE'])
@club_required
def delete_comentariu(activitate_id, comentariu_id):
    return club_controller.delete_comentariu(request.current_user, activitate_id, comentariu_id)

@club_bp.route('/threads', methods=['GET'])
@club_required
def get_club_threads():
    return club_controller.get_club_threads()

@club_bp.route('/threads', methods=['POST'])
@club_required
def create_club_thread():
    return club_controller.create_club_thread(request.current_user)

@club_bp.route('/threads/pending', methods=['GET'])
@bibliotecar_required
def get_pending_threads():
    return club_controller.get_pending_threads()

@club_bp.route('/threads/<int:thread_id>/approve', methods=['POST'])
@bibliotecar_required
def approve_club_thread(thread_id):
    return club_controller.approve_club_thread(thread_id)

@club_bp.route('/threads/<int:thread_id>', methods=['GET'])
@club_required
def get_club_thread(thread_id):
    return club_controller.get_club_thread(thread_id)

@club_bp.route('/threads/<int:thread_id>/comments', methods=['POST'])
@club_required
def add_thread_comment(thread_id):
    return club_controller.add_thread_comment(request.current_user, thread_id)

@club_bp.route('/threads/comments/<int:comentariu_id>/subcomments', methods=['POST'])
@club_required
def add_thread_subcomment(comentariu_id):
    return club_controller.add_thread_subcomment(request.current_user, comentariu_id)

@club_bp.route('/threads/comments/<int:comentariu_id>/like', methods=['POST'])
@club_required
def like_thread_comment(comentariu_id):
    return club_controller.like_thread_comment(comentariu_id)

@club_bp.route('/threads/subcomments/<int:subcomentariu_id>/like', methods=['POST'])
@club_required
def like_thread_subcomment(subcomentariu_id):
    return club_controller.like_thread_subcomment(subcomentariu_id)

@club_bp.route('/threads/<int:thread_id>', methods=['DELETE'])
@club_required
def delete_club_thread(thread_id):
    return club_controller.delete_club_thread(request.current_user, thread_id)

@club_bp.route('/threads/comments/<int:comentariu_id>', methods=['DELETE'])
@club_required
def delete_thread_comment(comentariu_id):
    return club_controller.delete_thread_comment(request.current_user, comentariu_id)

@club_bp.route('/threads/subcomments/<int:subcomentariu_id>', methods=['DELETE'])
@club_required
def delete_thread_subcomment(subcomentariu_id):
    return club_controller.delete_thread_subcomment(request.current_user, subcomentariu_id)
