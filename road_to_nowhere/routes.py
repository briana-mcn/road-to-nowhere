import json
import random
import string

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


def get_totals():
    song_count = db.session.query(SongModel).count()
    artist_count = db.session.query(ArtistModel).count()

    # db.session.query(SongModel)
    # db.session.query(ArtistModel)
    #
    # db.session.commit()
    # db.session.close()

    return artist_count, song_count


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
    return json.dumps(lyrics), 200


def get_random_lyrics():
    song_count = db.session.query(SongModel).count()
    random_choice = random.randint(0, song_count - 1)
    print(random_choice)
    song = db.session.query(SongModel)[random_choice]
    title = song.title
    artist = song.artist.name
    lyrics = song.lyrics.split('\n\n')
    db.session.close()
    return {
        'title': title,
        'artist': artist,
        'lyrics': random.choice(lyrics)
    }


@bp.route('/delete-song', methods=['DELETE'])
def delete_song():
    req_json = request.get_json()
    song_titled = string.capwords(req_json.get('song'))

    song_obj = db.session.query(SongModel).filter(SongModel.title == song_titled)
    song = song_obj.first()

    if not song:
        return json.dumps({"message": f"Failure: could not find '{song_titled}'"})
    else:
        formatted_song = repr(song)
        song_obj.delete()
        db.session.commit()
        db.session.close()
        return json.dumps({"message": f"Success: deleted: {formatted_song}"})


@bp.route('/songs', methods=['GET'])
def get_all_songs():
    songs = db.session.query(SongModel).all()

    results = []
    for song in songs:
        results.append(song.title)
    print(results)
    return json.dumps({'songs': results})
