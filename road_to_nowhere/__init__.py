from flask import Flask

from config import config_settings
from road_to_nowhere import routes
from road_to_nowhere.auth import auth_routes
from road_to_nowhere.database import db
from road_to_nowhere.helpers import register_blueprints

app = Flask(__name__)

app.config.from_object(config_settings)

register_blueprints(app, [routes.bp, auth_routes.bp])

db.init_app(app)
