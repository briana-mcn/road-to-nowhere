from flask import Flask

from config import config_settings
from road_to_nowhere import routes
from road_to_nowhere.database import db


app = Flask(__name__)
app.config.from_object(config_settings)

db.init_app(app)
app.register_blueprint(routes.bp)
