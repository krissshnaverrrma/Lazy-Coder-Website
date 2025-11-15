from flask import jsonify
from . import api_bp # Imports the blueprint defined in api/__init__.py

# --- API ROUTES ---

@api_bp.route('/', methods=['GET'])
def api_base():
    """
    Base route for the API.
    Accessed at /api/
    """
    return jsonify({
        'status': 'success',
        'message': 'Welcome to the Lazy Coder API subsystem.',
        'version': '1.0'
    }), 200


@api_bp.route('/status', methods=['GET'])
def api_status():
    """
    Health check or status route.
    Accessed at /api/status
    """
    # This checks if the Flask application is currently running
    return jsonify({
        'status': 'operational',
        'service': 'Lazy Coder Blog API'
    }), 200