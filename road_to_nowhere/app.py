# from road_to_nowhere import app
import os
from flask import Flask
from flask_login import LoginManager

from config import config_settings
from road_to_nowhere.database import db
from road_to_nowhere import routes
from road_to_nowhere.auth import auth_routes
from road_to_nowhere.helpers import register_blueprints
from road_to_nowhere.models import UserModel


def create_app():
    app = Flask(__name__)
    app.config.from_object(config_settings)
    register_blueprints(app, [routes.bp, auth_routes.bp])
    db.init_app(app)

    # login manager required configs
    login = LoginManager(app)

    @login.user_loader
    def load_user(id):
        return UserModel.query.get(int(id))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=os.getenv('ROAD_TO_NOWHERE_PORT'),  debug=os.getenv('DEBUG_WEB_SERVER'))
