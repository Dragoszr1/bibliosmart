from flask import Blueprint, request
from app.middlewares.auth import jwt_required
from app.controllers import ai_controller

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/recommend', methods=['GET'])
@jwt_required
def ai_recommend():
    return ai_controller.ai_recommend(request.current_user)

@ai_bp.route('/review-assist', methods=['POST'])
@jwt_required
def ai_review_assist():
    return ai_controller.ai_review_assist()

@ai_bp.route('/book-summary/<int:carte_id>', methods=['GET'])
@jwt_required
def ai_book_summary(carte_id):
    return ai_controller.ai_book_summary(carte_id)

@ai_bp.route('/chat', methods=['POST'])
@jwt_required
def ai_chat():
    return ai_controller.ai_chat()
