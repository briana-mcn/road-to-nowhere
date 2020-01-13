import json
from random import random

from flask import Blueprint, request
from tswift import Artist
from tswift import Song

from road_to_nowhere.models import SongModel, ArtistModel


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
    artist = request.get_json().get('artist')
    song = request.get_json().get('song')
    try:
        parsed_song = Song(title=song, artist=artist)
    except ValueError:
        return 'Invalid Song or Artist requested: {}'.format(parsed_song), 400
    else:
        if parsed_song.lyrics != "":
            # add song
            return json.dumps(parsed_song.lyrics), 200
        
