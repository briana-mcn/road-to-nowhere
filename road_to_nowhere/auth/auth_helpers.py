from flask import request
from sqlalchemy.exc import SQLAlchemyError

from road_to_nowhere import login_manager
from road_to_nowhere.database import db
from road_to_nowhere.exceptions import DatabaseRoadToNowhereError
from road_to_nowhere.models import UserModel


def get_user_data():
    body = request.get_json()
    username = None
    password = None

    if body:
        username = body.get('username')
        password = body.get('password', '').encode()
    return username, password


def add_user(username, password):
    if get_user(username):
        raise DatabaseRoadToNowhereError('Username already exists')

    try:
        user = UserModel(username=username, password=password)
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise
    finally:
        db.session.close()


def get_user(username):
    user = db.session.query(UserModel).filter(UserModel.username == username).first()
    return user


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))
