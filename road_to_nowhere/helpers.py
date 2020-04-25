import string
from road_to_nowhere.exceptions import RequestValidationError


def validate_song_and_artist(request):
    request_body = request.get_json()
    artist = request_body.get('artist')
    song = request_body.get('song')

    if not artist or not song:
        raise RequestValidationError('Song or artist must be a provided or a valid string sequence')

    artist = string.capwords(artist)
    song = string.capwords(song)

    return artist, song


def register_blueprints(flask_app, blueprints):
    for blueprint in blueprints:
        flask_app.register_blueprint(blueprint)
