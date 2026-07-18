from flask import Blueprint, request
from app.middlewares.auth import jwt_required, bibliotecar_required
from app.controllers import books_controller

books_bp = Blueprint('books', __name__)
requests_bp = Blueprint('book_requests', __name__)

@books_bp.route('/', methods=['GET'])
def get_books():
    return books_controller.get_books()

@books_bp.route('/recent', methods=['GET'])
def get_recent_books():
    return books_controller.get_recent_books()

@books_bp.route('/', methods=['POST'])
@bibliotecar_required
def add_book():
    return books_controller.add_book()

@books_bp.route('/<int:carte_id>', methods=['PUT'])
@bibliotecar_required
def update_book(carte_id):
    return books_controller.update_book(carte_id)

@books_bp.route('/<int:carte_id>', methods=['DELETE'])
@bibliotecar_required
def delete_book(carte_id):
    return books_controller.delete_book(carte_id)

@books_bp.route('/<int:carte_id>/request-fizic', methods=['POST'])
@jwt_required
def request_book_fizic(carte_id):
    return books_controller.request_book_fizic(request.current_user, carte_id)

@requests_bp.route('/', methods=['GET'])
@bibliotecar_required
def get_book_requests():
    return books_controller.get_book_requests()

@requests_bp.route('/<int:cerere_id>', methods=['PUT'])
@bibliotecar_required
def update_book_request(cerere_id):
    return books_controller.update_book_request(cerere_id)

@requests_bp.route('/<int:cerere_id>/confirma-ridicare', methods=['POST'])
@bibliotecar_required
def confirma_ridicare(cerere_id):
    return books_controller.confirma_ridicare(cerere_id)

@books_bp.route('/image', methods=['POST'])
@bibliotecar_required
def upload_book_image():
    return books_controller.upload_book_image()

@books_bp.route('/image/<int:carte_id>', methods=['GET'])
def get_book_image(carte_id):
    return books_controller.get_book_image(carte_id)

@books_bp.route('/pdf', methods=['POST'])
@bibliotecar_required
def upload_book_pdf():
    return books_controller.upload_book_pdf()

@books_bp.route('/pdf/<int:carte_id>', methods=['GET'])
@jwt_required
def get_book_pdf(carte_id):
    return books_controller.get_book_pdf(carte_id)

@books_bp.route('/pdf/<int:carte_id>', methods=['DELETE'])
@bibliotecar_required
def delete_book_pdf(carte_id):
    return books_controller.delete_book_pdf(carte_id)

