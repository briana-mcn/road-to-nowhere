import json

from flask import Blueprint, request
from flask_login import login_required
from tswift import TswiftError

from road_to_nowhere import songs_and_artists
from road_to_nowhere.exceptions import DatabaseRoadToNowhereError, RequestValidationError, RoadToNowhereError
from road_to_nowhere.helpers import validate_song_and_artist

bp = Blueprint('song_builder', __name__)


@bp.route('/song', methods=['GET', 'POST'])
@login_required
def song():
    """Creates or retrieves a song and artist if they are valid requests.

    Expects the following format for the request body:
    {
        'song': str,
        'artist': str
    }
    """
    try:
        artist_name, song_title = validate_song_and_artist(request)
    except RequestValidationError as e:
        return json.dumps({"message": e.msg}), 400

    if request.method == 'POST':
        try:
            results = songs_and_artists.create_song(artist_name, song_title)

        except ValueError:
            return json.dumps(
                {
                    "message": "Invalid Song or Artist requested",
                    "artist": artist_name,
                    "song": song_title
                }
            ), 400

        except DatabaseRoadToNowhereError as e:
            return json.dumps({"message": e.msg}), 200

        except TswiftError:
            return json.dumps({"message": "Unable to handle the artist and song combo"}), 500

        else:
            results.update({"message": "Song created"})
            return json.dumps(results), 201

    if request.method == 'GET':
        try:
            results = songs_and_artists.retrieve_song_and_lyrics(artist_name, song_title)
        except DatabaseRoadToNowhereError as e:
            return json.dumps({"message": e.msg}), 400
        else:
            return json.dumps(results)


@bp.route('/random', methods=['GET'])
def random_lyrics():
    """Retrieves a random refrain from a song.

    Requires a song and artist string as the request body in the following format:
    {
        'song': str,
        'artist': str
    }
    """
    try:
        song_data = songs_and_artists.get_random_lyrics()
    except RoadToNowhereError as e:
        return json.dumps({"message": "No songs found"})
    else:
        return json.dumps(song_data)


@bp.route('/delete-song', methods=['DELETE'])
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
        artist_name, song_title = validate_song_and_artist(request)
    except RequestValidationError as e:
        return json.dumps({"message": e.msg}), 400

    try:
        songs_and_artists.delete_requested_song(artist_name, song_title)
    except DatabaseRoadToNowhereError as e:
        return json.dumps({"message": e.msg}), 400

    return json.dumps({"message": f"Success: Deleted '{song_title}' by {artist_name}'"}), 200


@bp.route('/songs', methods=['GET'])
def get_all_songs():
    """Returns all songs written to the database."""
    return json.dumps(songs_and_artists.get_all_songs()), 200


@bp.route('/artists', methods=['GET'])
def get_all_artists():
    """Returns all artists written to the database."""
    return json.dumps(songs_and_artists.get_all_artists()), 200
