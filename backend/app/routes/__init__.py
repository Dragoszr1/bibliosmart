from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__, url_prefix='/api')

@main_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Server is running'}), 200

@main_bp.route('/', methods=['GET'])
def index():
    return jsonify({
        'name': 'API site biblioteca CNI Suceava',
        'version': '1.0.0',
        'message': 'Database connection established'
    }), 200

@main_bp.route('/csrf-token', methods=['GET'])
def get_csrf_token():
    from flask_wtf.csrf import generate_csrf
    return jsonify({'csrfToken': generate_csrf()}), 200
