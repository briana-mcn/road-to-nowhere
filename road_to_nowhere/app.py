from flask import Flask

from config import config_settings
from road_to_nowhere import login_manager
from road_to_nowhere.routes import song_routes, auth_routes
from road_to_nowhere.helpers import register_blueprints


def create_app():
    app = Flask(__name__)
    app.config.from_object(config_settings)

    from road_to_nowhere.database import db
    db.init_app(app)

    login_manager.init_app(app)
    register_blueprints(app, [song_routes.bp, auth_routes.bp])

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=config_settings.ROAD_TO_NOWHERE_PORT,  debug=True)
