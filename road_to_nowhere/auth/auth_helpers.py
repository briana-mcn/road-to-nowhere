from flask import request
from sqlalchemy.exc import SQLAlchemyError

from road_to_nowhere import db
from road_to_nowhere.exceptions import DatabaseRoadToNowhereError
from road_to_nowhere.models import UserModel


def get_user_data():
    body = request.get_json()
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
