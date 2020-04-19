import json

from cryptography.exceptions import InvalidKey
from flask import Blueprint
from flask_login import current_user, login_user, logout_user

from road_to_nowhere.auth.auth_helpers import add_user, get_user, get_user_data
from road_to_nowhere.exceptions import DatabaseRoadToNowhereError

bp = Blueprint('auth_manager', __name__)


@bp.route('/register-user', methods=['POST'])
def register():
    username, password = get_user_data()
    if not username or not password:
        return json.dumps({"message": "Must supply valid username and password"}), 400
    try:
        add_user(username, password)
    except DatabaseRoadToNowhereError:
        return json.dumps({"message": "User already exists"}), 400
    return json.dumps({"message": "Successfully added user"}), 200


@bp.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return {'message': 'User is already logged in'}, 200

    username, password = get_user_data()
    user = get_user(username)

    if user is None or password is None:
        return {'message': 'Username and password is required to log in'}, 400

    try:
        user.verify_hash(password)
    except InvalidKey:
        return {'message': 'Incorrect Username or password'}, 404

    login_user(user, remember=True)
    return {'message': 'Logged in'}, 200


@bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return {'message': 'Logged out'}, 200
