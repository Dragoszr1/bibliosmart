from flask import Blueprint, request
from app.middlewares.auth import jwt_required
from app.controllers import auth_controller

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    return auth_controller.login()

@auth_bp.route('/verify-code', methods=['POST'])
def verify_code():
    return auth_controller.verify_code()

@auth_bp.route('/me', methods=['GET'])
@jwt_required
def auth_me():
    return auth_controller.auth_me(request.current_user)

@auth_bp.route('/logout', methods=['POST'])
def logout():
    return auth_controller.logout()

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    return auth_controller.forgot_password()

@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    return auth_controller.reset_password(token)

@auth_bp.route('/profile', methods=['GET'])
@jwt_required
def profile():
    return auth_controller.profile(request.current_user)

@auth_bp.route('/books-read', methods=['GET'])
@jwt_required
def books_read():
    return auth_controller.books_read(request.current_user)

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required
def update_profile():
    return auth_controller.update_profile(request.current_user)

@auth_bp.route('/register', methods=['POST'])
def register():
    return auth_controller.register()

@auth_bp.route('/verify-register', methods=['POST'])
def verify_register():
    return auth_controller.verify_register()

@auth_bp.route('/profile-picture', methods=['POST'])
@jwt_required
def upload_profile_picture():
    return auth_controller.upload_profile_picture(request.current_user)

@auth_bp.route('/profile-picture/<username>', methods=['GET'])
def get_profile_picture(username):
    return auth_controller.get_profile_picture(username)
