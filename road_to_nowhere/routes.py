import json

from flask import Blueprint, request

from road_to_nowhere import songs_and_artists
from road_to_nowhere.exceptions import RoadToNowhereError
from road_to_nowhere.helpers import get_requested_artist_and_song

bp = Blueprint('song_builder', __name__)


@bp.route('/song', methods=['POST'])
def post_song():
    """Creates a song and artist if they are valid requests.

    Expects the following format for the request body:
    {
        'song': str,
        'artist': str
    }
    """
    artist, song = get_requested_artist_and_song()

    try:
        artist_obj, song_obj = songs_and_artists.create_song(artist, song)

    except ValueError:
        return json.dumps({"message": "Invalid Song or Artist requested",  "artist": artist, "song": song}), 400

    except RoadToNowhereError:
        return json.dumps(
            {
                "message": "No lyrics found for requested song and artist combination",
                "artist": artist,
                "song": song
             }), 500

    else:
        return json.dumps(
            {
                "message": "Success",
                "song": song_obj.title,
                "artist": artist_obj.name,
                "lyrics": song_obj.lyrics
            }), 201


@bp.route('/random', methods=['GET'])
def random_lyrics():
    return json.dumps(songs_and_artists.get_random_lyrics()), 200


@bp.route('/delete-song', methods=['DELETE'])
def delete_song():
    artist, song = get_requested_artist_and_song()

    success, song_obj = songs_and_artists.delete_requested_song(artist, song)
    if not success:
        return json.dumps({"message": f"Failure: could not find '{song}' by '{artist}'"}), 400
    else:
        return json.dumps({"message": f"Success: Deleted '{song}' by {artist}'"}), 200


@bp.route('/songs', methods=['GET'])
def get_all_songs():
    return json.dumps(songs_and_artists.get_all_songs()), 200
