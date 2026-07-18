from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__, url_prefix='/api')

@main_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Server is running'}), 200

@main_bp.route('/', methods=['GET'])
def index():
    return jsonify({
        'name': 'API site biblioteca CNI Suceava',
        'version': 'idk(forgot to count lol)',
        'message': 'Database connection established'
    }), 200
