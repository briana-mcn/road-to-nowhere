from flask import request


def get_requested_artist_and_song():
    req_json = request.get_json()
    return req_json.get('artist'), req_json.get('song')


def register_blueprints(flask_app, blueprints):
    for blueprint in blueprints:
        flask_app.register_blueprint(blueprint)
