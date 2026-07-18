from flask import Blueprint, request
from app.middlewares.auth import jwt_required, bibliotecar_required
from app.controllers import anunturi_controller

anunturi_bp = Blueprint('anunturi', __name__)

@anunturi_bp.route('/', methods=['GET'])
def get_anunturi():
    return anunturi_controller.get_anunturi()

@anunturi_bp.route('/', methods=['POST'])
@bibliotecar_required
def create_anunt():
    return anunturi_controller.create_anunt()

@anunturi_bp.route('/<int:anunt_id>', methods=['PUT'])
@bibliotecar_required
def update_anunt(anunt_id):
    return anunturi_controller.update_anunt(anunt_id)

@anunturi_bp.route('/<int:anunt_id>', methods=['DELETE'])
@bibliotecar_required
def delete_anunt(anunt_id):
    return anunturi_controller.delete_anunt(anunt_id)

@anunturi_bp.route('/<int:anunt_id>/like', methods=['POST'])
@jwt_required
def toggle_like_anunt(anunt_id):
    return anunturi_controller.toggle_like_anunt(request.current_user, anunt_id)
