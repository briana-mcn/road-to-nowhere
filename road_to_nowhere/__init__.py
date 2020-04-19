from flask import Flask
from flask_login import LoginManager

from config import config_settings
from road_to_nowhere.database import db
from road_to_nowhere import routes
from road_to_nowhere.auth import auth_routes
from road_to_nowhere.helpers import register_blueprints
from road_to_nowhere.models import UserModel

app = Flask(__name__)
app.config.from_object(config_settings)
register_blueprints(app, [routes.bp, auth_routes.bp])
db.init_app(app)

# login manager required configs
login = LoginManager(app)

@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))
