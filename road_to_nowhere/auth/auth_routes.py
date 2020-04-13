import json

from cryptography.exceptions import InvalidKey
from flask import Blueprint

from road_to_nowhere.auth.auth_helpers import add_user, get_user, get_user_data
from road_to_nowhere.exceptions import DatabaseRoadToNowhereError

bp = Blueprint('login_manager', __name__)


@bp.route('/register-user', methods=['POST'])
def register():
    username, password = get_user_data()
    try:
        add_user(username, password)
    except DatabaseRoadToNowhereError:
        return json.dumps({"message": "User already exists"}), 400
    return json.dumps({"message": "Successfully added user"}), 200


@bp.route('/login', methods=['GET'])
def login():
    username, password = get_user_data()
    user = get_user(username)
    try:
        user.verify_hash(password)
    except InvalidKey:
        return {'message': 'Incorrect Username or password'}, 404
    return {'message': 'logged in'}, 200
