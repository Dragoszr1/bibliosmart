from flask import Blueprint
from app.middlewares.auth import bibliotecar_required
from app.controllers import admin_controller

admin_bp = Blueprint('admin', __name__)
librarian_bp = Blueprint('librarian', __name__)

@librarian_bp.route('/report/docx', methods=['GET'])
@bibliotecar_required
def librarian_report_docx():
    return admin_controller.librarian_report_docx()

@admin_bp.route('/users', methods=['GET'])
@bibliotecar_required
def admin_get_users():
    return admin_controller.admin_get_users()

@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@bibliotecar_required
def admin_get_user_detail(user_id):
    return admin_controller.admin_get_user_detail(user_id)

@admin_bp.route('/loans/<int:imprumut_id>/prelungeste', methods=['PUT'])
@bibliotecar_required
def prelungeste_imprumut(imprumut_id):
    return admin_controller.prelungeste_imprumut(imprumut_id)

@admin_bp.route('/loans/<int:imprumut_id>/returneaza', methods=['POST'])
@bibliotecar_required
def returneaza_imprumut(imprumut_id):
    return admin_controller.returneaza_imprumut(imprumut_id)
