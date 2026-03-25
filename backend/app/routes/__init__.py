from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__, url_prefix='/api')

@main_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Server is running'}), 200

@main_bp.route('/', methods=['GET'])
def index():
    """API index"""
    return jsonify({
        'name': 'School Library API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health'
        }
    }), 200
