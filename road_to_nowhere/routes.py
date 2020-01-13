from flask import Blueprint, request


bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    return 'Hello World!'
