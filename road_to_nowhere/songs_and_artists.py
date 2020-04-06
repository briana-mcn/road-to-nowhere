import random
import string

from tswift import Song

from road_to_nowhere import db
from road_to_nowhere.models import SongModel, ArtistModel
from road_to_nowhere.exceptions import RoadToNowhereError


def get_all_songs():
    songs = db.session.query(SongModel).all()

    results = []
    for song in songs:
        results.append({
            'song': song.title,
            'artist': song.artist.name,
            'lyrics': song.lyrics,
        })

    return {'songs': results}


def delete_requested_song(artist, song):
    song_titled = string.capwords(song)
    artist_titled = string.capwords(artist)

    artist_obj = db.session.query(ArtistModel).filter(
        ArtistModel.name == artist_titled,
    ).first()

    song_obj = db.session.query(SongModel).filter(
        SongModel.artist == artist_obj,
        SongModel.title == song_titled
    )
    song = song_obj.first()

    if not song:
        success = False
    else:
        song_obj.delete()
        db.session.commit()
        db.session.close()
        success = True

    return success, song_obj


def get_random_lyrics():
    song_count = db.session.query(SongModel).count()
    random_choice = random.randint(0, song_count - 1)
    song = db.session.query(SongModel)[random_choice]
    title = song.title
    artist = song.artist.name
    lyrics = song.lyrics.split('\n\n')
    lyrics = [lyric for lyric in lyrics if lyric]
    db.session.close()
    return {
        'title': title,
        'artist': artist,
        'lyrics': random.choice(lyrics)
    }


def create_song(artist, song):

    parsed_song = Song(title=song, artist=artist)
    _validate_song(parsed_song)
    create_song_and_artist(parsed_song)

    artist_obj, song_obj = query_artist_and_song_objects(parsed_song)

    return artist_obj, song_obj,


def _validate_song(results_body):
    if not results_body.lyrics:
        raise RoadToNowhereError('No lyrics returned from the Songs API')


def get_artist_and_song_totals():
    song_count = db.session.query(SongModel).count()
    artist_count = db.session.query(ArtistModel).count()

    return artist_count, song_count


def query_artist_and_song_objects(parsed_song):
    artist = db.session.query(ArtistModel).filter(ArtistModel.name == parsed_song.artist).first()
    song = db.session.query(SongModel).filter(
        SongModel.artist == artist,
        SongModel.title == parsed_song.title
    ).first()

    return artist, song


def create_song_and_artist(parsed_song):
    artist, song = query_artist_and_song_objects(parsed_song)

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

