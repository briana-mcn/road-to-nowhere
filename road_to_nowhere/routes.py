import json

from flask import Blueprint

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
                "message": "Successfully created or retrieved song and artist",
                "song": song_obj.title,
                "artist": artist_obj.name,
                "lyrics": song_obj.lyrics
            }), 201


@bp.route('/random', methods=['GET'])
def random_lyrics():
    """Retrieves a random refrain from the `SongModel` table."""
    return json.dumps(songs_and_artists.get_random_lyrics()), 200


@bp.route('/delete-song', methods=['DELETE'])
def delete_song():
    """Deletes only a song if the song and artist combo exist.

    Expects the following format for the request body:
    {
        'song': str,
        'artist': str
    }
    """
    artist, song = get_requested_artist_and_song()
    success = songs_and_artists.delete_requested_song(artist, song)

    if not success:
        return json.dumps({"message": f"Failure: could not find '{song}' by '{artist}'"}), 400
    else:
        return json.dumps({"message": f"Success: Deleted '{song}' by {artist}'"}), 200


@bp.route('/songs', methods=['GET'])
def get_all_songs():
    """Returns all songs written to the database."""
    return json.dumps(songs_and_artists.get_all_songs()), 200
