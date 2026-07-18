from flask import Blueprint, request
from app.middlewares.auth import jwt_required
from app.controllers import reviews_controller

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/', methods=['GET'])
def get_reviews():
    return reviews_controller.get_reviews()

@reviews_bp.route('/', methods=['POST'])
@jwt_required
def submit_review():
    return reviews_controller.submit_review(request.current_user)

@reviews_bp.route('/user', methods=['GET'])
@jwt_required
def get_user_reviews():
    return reviews_controller.get_user_reviews(request.current_user)
