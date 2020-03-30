import json

from flask import Blueprint, request
from tswift import Song

from road_to_nowhere.models import SongModel, ArtistModel
from road_to_nowhere import db


bp = Blueprint('song_builder', __name__)


@bp.route('/song', methods=['POST'])
# expects artist and song name in json body
# builds these objects and commits them to the db
# returns okay status if the song was built
# body = {
    #     'song': str,
    #     'artist': str
# }
def post_song():
    req_json = request.get_json()
    artist = req_json.get('artist')
    song = req_json.get('song')
    try:
        parsed_song = Song(title=song, artist=artist)
    except ValueError:
        return f'Invalid Song or Artist requested: {artist, song}', 400
    else:
        if parsed_song.lyrics != "":
            write_song(parsed_song)
            return json.dumps(parsed_song.lyrics), 200
        else:
            return f'Song and Artist combination not found: {artist, song}', 400


def write_song(parsed_song):
    try:
        artist = ArtistModel(name=parsed_song.artist)
        song = SongModel(title=parsed_song.title, lyrics=parsed_song.lyrics, artist=artist)
        db.session.add_all([song, artist])
        db.session.commit()
    except Exception:
        pass
        db.session.rollback()
        raise
    finally:
        pass
        db.session.close()
