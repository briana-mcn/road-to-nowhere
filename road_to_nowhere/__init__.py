import os

from flask import Flask

from road_to_nowhere import routes
import config


def create_app():
    app = Flask(__name__)

    run_mode = os.environ.get('RUN_MODE', "dev")

    if  run_mode == 'dev':
        app.config.from_object(config.ConfigDev)

    elif run_mode == 'prod':
        app.config.from_object(config.ConfigProd)

    elif run_mode == 'test':
        app.config.from_object(config.ConfigTest)

    app.register_blueprint(routes.bp)

    return app
