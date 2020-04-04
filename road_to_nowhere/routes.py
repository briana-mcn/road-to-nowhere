import json
import random

from flask import Blueprint, request
from tswift import Song

from road_to_nowhere.models import SongModel, ArtistModel
from road_to_nowhere import db


bp = Blueprint('song_builder', __name__)


@bp.route('/song', methods=['POST'])
def post_song():
    """# expects artist and song name in json body
    # builds these objects and commits them to the db
    # returns okay status if the song was built
    # body = {
        #     'song': str,
        #     'artist': str
    }
    """
    req_json = request.get_json()
    artist = req_json.get('artist')
    song = req_json.get('song')

    try:
        parsed_song = Song(title=song, artist=artist)
        get_song_and_artist_models(parsed_song)
    except ValueError:
        return f'Invalid Song or Artist requested: {artist, song}', 400

    artist, song = query_objects(parsed_song)

    return json.dumps({'message': 'Success', 'artist': artist.name, 'song': song.title}), 200


def query_objects(parsed_song):
    artist = db.session.query(ArtistModel).filter(ArtistModel.name == parsed_song.artist).first()
    song = db.session.query(SongModel).filter(
        SongModel.artist == artist,
        SongModel.title == parsed_song.title
    ).first()

    return artist, song


def get_song_and_artist_models(parsed_song):
    artist, song = query_objects(parsed_song)

    if artist is None:
        artist = build_artist(parsed_song)
        db.session.add(artist)
    if song is None:
        song = build_song(parsed_song, artist)
        db.session.add(song)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()


def build_artist(parsed_song):
    return ArtistModel(name=parsed_song.artist)


def build_song(parsed_song, artist):
    return SongModel(title=parsed_song.title, lyrics=parsed_song.lyrics, artist=artist)


@bp.route('/random', methods=['GET'])
def random_lyrics():
    lyrics = get_random_lyrics()
    return lyrics, 200


def get_random_lyrics():
    song_count = db.session.query(SongModel).count()
    random_choice = random.randint(0, song_count)
    song = db.session.query(SongModel)[random_choice]
    title = song.title
    artist = song.artist.name
    lyrics = song.lyrics.split('\n\n')
    db.session.close()
    return json.dumps({
        'title': title,
        'artist': artist,
        'lyrics': random.choice(lyrics)
    })
