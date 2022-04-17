import json

from flask import Blueprint
from flask_login import login_required
from tswift import TswiftError

from road_to_nowhere import request_models
from road_to_nowhere.exceptions import DatabaseRoadToNowhereError, RequestValidationError, RoadToNowhereError
from road_to_nowhere.helpers import get_request_model, get_post_request_model
from road_to_nowhere.api.songs_and_artists import SongHandler, SongWriter

api_bp = Blueprint('song_builder', __name__)


@api_bp.route('/song', methods=['POST'])
@login_required
def post_song():
    """Creates song and artist if the request is valid.

    Expects the following format for the request body:
    {
        'song': str,
        'artist': str
    }
    """

    try:
        request_model = get_post_request_model(request_models.SongRequestModel, ['song', 'artist'])
    except RequestValidationError as e:
        return json.dumps({"message": e.msg}), 400

    try:
        results = SongWriter().create_song(request_model.song, request_model.artist)
    except DatabaseRoadToNowhereError as e:
        return json.dumps({"message": str(e)}), 200
    except TswiftError as e:
        return json.dumps({"message": str(e)}), 500
    else:
        return results, 201


@api_bp.route('/song', methods=['GET'])
def get_song():
    """Retrieves a song and artist if they are valid requests.

    Expects the following format for the query parameter:
    ?song=<valid-song>&artist=<valid-artist>
    """

    try:
        request_model = get_request_model(request_models.SongRequestModel, ['artist', 'song'])
    except RequestValidationError as e:
        return json.dumps({"message": e.msg}), 400

    try:
        result = SongHandler().get_song(request_model.song, request_model.artist)
    except DatabaseRoadToNowhereError as e:
        return json.dumps({"message": e.msg}), 400
    else:
        return result, 200


@api_bp.route('/random', methods=['GET'])
def random_lyrics():
    """Retrieves a random refrain from any song."""
    try:
        song_data = SongHandler().get_random_lyrics()
    except RoadToNowhereError as e:
        return json.dumps({"message": "No songs found"})
    else:
        return json.dumps(song_data)


@api_bp.route('/delete-song', methods=['DELETE'])
@login_required
def delete_song():
    """Deletes only a song if the song and artist combo exist.

    Expects the following format for the request body:
    {
        'song': str,
        'artist': str
    }
    """
    try:
        request_model = get_post_request_model(request_models.SongRequestModel, ['artist', 'song'])
    except RequestValidationError as e:
        return json.dumps({"message": e.msg}), 400

    try:
        result = SongHandler().delete_song(request_model.song, request_model.artist)
    except DatabaseRoadToNowhereError as e:
        return json.dumps({"message": e.msg}), 400

    return json.dumps({"deleted": result}), 200


@api_bp.route('/songs', methods=['GET'])
def get_all_songs():
    """Returns all songs written to the database."""
    return json.dumps(SongHandler().get_all_songs()), 200


@api_bp.route('/artists', methods=['GET'])
def get_all_artists():
    """Returns all artists written to the database."""
    return json.dumps(SongHandler().get_all_artists()), 200
