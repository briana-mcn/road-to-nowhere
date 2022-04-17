import os

from flask import Flask
from flask_login import LoginManager

from config import config_settings
from road_to_nowhere.api.routes import api_bp
from road_to_nowhere.auth.routes import auth_bp
from road_to_nowhere.database import db
from road_to_nowhere.helpers import register_blueprints
from road_to_nowhere.models import UserModel


def create_app():
    app = Flask(__name__)
    app.config.from_object(config_settings)
    register_blueprints(app, [api_bp, auth_bp])
    db.init_app(app)

    # login manager required configs
    login = LoginManager(app)

    # takes user id from current session and logs them in
    @login.user_loader
    def load_user(id):
        return UserModel.query.get(int(id))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=os.getenv('ROAD_TO_NOWHERE_PORT'),  debug=os.getenv('DEBUG_WEB_SERVER'))
