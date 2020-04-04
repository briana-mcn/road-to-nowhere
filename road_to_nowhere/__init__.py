from flask import Flask

from config import config_settings
from road_to_nowhere.database import db
from road_to_nowhere import routes

app = Flask(__name__)
app.config.from_object(config_settings)

app.register_blueprint(routes.bp)

db.init_app(app)
