import random

from tswift import Song

from road_to_nowhere import db
from road_to_nowhere.models import SongModel, ArtistModel
from road_to_nowhere.exceptions import DatabaseRoadToNowhereError, RoadToNowhereError


def retrieve_all_songs(session):
    return session.query(SongModel).all()


def retrieve_artist(session, artist_name):
    return session.query(ArtistModel).filter(
        ArtistModel.name == artist_name,
    ).first()


def retrieve_song(session, song_title, artist_id=None):
    if artist_id:
        return session.query(SongModel).filter(
                SongModel.title == song_title,
                SongModel.artist_id == artist_id
        ).first()
    else:
        return session.query(SongModel).filter(
            SongModel.title == song_title,
        ).first()


def retrieve_song_and_lyrics(artist_name, song_title):
    session = db.session()
    artist = retrieve_artist(session, artist_name)

    if artist is None:
        raise DatabaseRoadToNowhereError(f'No artist found:  {artist_name}')

    song = retrieve_song(session, song_title, artist.id)

    if song is None:
        raise DatabaseRoadToNowhereError(f'No song found: {song_title} by {artist_name}')

    return {'artist': artist.name, 'song': song.title, 'lyrics': song.lyrics}


def create_song(artist_name, song_title):
    session = db.session()
    song = None

    artist = retrieve_artist(session, artist_name)
    if artist:
        song = retrieve_song(session, song_title, artist.id)

    if song:
        raise DatabaseRoadToNowhereError(f'Song already exists: {song.title} by {song.artist.name}')

    parsed_song = Song(title=song_title, artist=artist_name)
    validate_song(parsed_song)

    song = build_song(session, song_title, parsed_song.lyrics, artist)
    results = {'artist': artist.name, 'song': song.title, 'lyrics': song.lyrics}

    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

    return results


def get_all_songs():
    results = []
    for song in retrieve_all_songs(db.session()):
        results.append({
            'song': song.title,
            'artist': song.artist.name,
            'lyrics': song.lyrics,
        })

    return {'songs': results}


def delete_requested_song(artist_name, song_title):
    session = db.session()

    artist = retrieve_artist(session, artist_name)
    if artist is None:
        raise DatabaseRoadToNowhereError(f'No artist found:  {artist_name}')

    song = retrieve_song(session, song_title, artist.id)
    if song is None:
        raise DatabaseRoadToNowhereError(f'Song was not found: {song_title} by {artist_name}')

    session.delete(song)

    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

    return True


def get_random_lyrics():
    session = db.session()
    all_songs = retrieve_all_songs(session)

    if not all_songs:
        raise RoadToNowhereError('No songs found')

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


def validate_song(parsed_song):
    if not parsed_song.lyrics:
        raise RoadToNowhereError('No lyrics returned from the Songs API')


def get_artist_and_song_totals():
    song_count = db.session.query(SongModel).count()
    artist_count = db.session.query(ArtistModel).count()

    return artist_count, song_count


def build_artist(session, artist_name):
    artist = ArtistModel(name=artist_name)
    session.add(artist)
    return artist


def build_song(session, song_title, song_lyrics, artist):
    song = SongModel(title=song_title, lyrics=song_lyrics, artist=artist)
    session.add(song)
    return song


def get_all_artists():
    artists = db.session.query(ArtistModel).all()
    all_artists = []
    for artist in artists:
        all_artists.append(artist.name)
    return {'artists': all_artists}
