import random
import string

from tswift import Song

from road_to_nowhere import db
from road_to_nowhere.models import SongModel, ArtistModel
from road_to_nowhere.exceptions import RoadToNowhereError


def retrieve_all_songs(session):
    return session.query(SongModel).all()


def retrieve_artist(session, artist_name):
    return session.query(ArtistModel).filter(
        ArtistModel.name == artist_name,
    )


def retrieve_song(session, song_title, artist_id):
    return session.query(SongModel).filter(
            SongModel.title == song_title,
            SongModel.artist_id == artist_id
    )


def retrieve_artist_and_song(session, parsed_song):
    artist = retrieve_artist(session, parsed_song.artist)
    artist = artist.first()
    song = retrieve_song(session, parsed_song.title, artist.id)
    song = song.first()

    return artist, song


def get_all_songs():
    results = []
    for song in retrieve_all_songs(db.session()):
        results.append({
            'song': song.title,
            'artist': song.artist.name,
            'lyrics': song.lyrics,
        })

    return {'songs': results}


def delete_requested_song(artist, song):
    song = string.capwords(song)
    artist = string.capwords(artist)
    session = db.session()

    artist_obj = retrieve_artist(session, artist)
    artist_obj = artist_obj.first()
    song_obj = retrieve_song(session, song, artist_obj.id)

    if not song_obj.first():
        success = False
    else:
        song_obj.delete()
        session.commit()
        session.close()
        success = True

    return success


def get_random_lyrics():
    session = db.session()

    all_songs = retrieve_all_songs(session)
    song_count = len(all_songs)
    random_choice = random.randint(0, song_count - 1)

    song = all_songs[random_choice]
    lyrics = song.lyrics.split('\n\n')
    lyrics = [lyric for lyric in lyrics if lyric]

    return {
        'title': song.title,
        'artist': song.artist.name,
        'lyrics': random.choice(lyrics)
    }


def create_song(artist, song):

    parsed_song = Song(title=song, artist=artist)
    validate_song(parsed_song)
    session = db.session()

    create_song_and_artist(parsed_song)

    artist_obj, song_obj = retrieve_artist_and_song(session, parsed_song)

    return artist_obj, song_obj,


def validate_song(parsed_song):
    if not parsed_song.lyrics:
        raise RoadToNowhereError('No lyrics returned from the Songs API')


def get_artist_and_song_totals():
    song_count = db.session.query(SongModel).count()
    artist_count = db.session.query(ArtistModel).count()

    return artist_count, song_count


def create_song_and_artist(parsed_song):
    session = db.session()
    artist, song = retrieve_artist_and_song(session, parsed_song)

    if artist is None:
        artist = build_artist(session, parsed_song)

    if song is None:
        build_song(session, parsed_song, artist)

    try:
        db.session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def build_artist(session, parsed_song):
    artist = ArtistModel(name=parsed_song.artist)
    session.add(artist)
    return artist


def build_song(session, parsed_song, artist):
    song = SongModel(title=parsed_song.title, lyrics=parsed_song.lyrics, artist=artist)
    session.add(song)
    return song

