from flask import Blueprint

# Define the Blueprint for the API subsystem
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Import the routes defined in index.py so they are registered with the Blueprint
from . import index