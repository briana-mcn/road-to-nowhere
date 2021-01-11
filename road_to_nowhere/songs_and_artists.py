import random

from tswift import Song

from road_to_nowhere.database import db
from road_to_nowhere.models import SongModel, ArtistModel
from road_to_nowhere.exceptions import DatabaseRoadToNowhereError, RoadToNowhereError
from road_to_nowhere.response_models import (
    ArtistResponseModel,
    SongResponseModel,
    MultipleArtistsResponseModel,
    MultipleSongsResponseModel
)


class SongWriter:
    def __init__(self):
        self.session = db.session()
        self.handler = SongHandler(self.session)
        self._song = None
        self._artist = None
        self._lyrics = None

    @property
    def song(self):
        return self._song

    @property
    def artist(self):
        return self._artist

    def lyrics(self):
        return self._lyrics

    def create_song(self, song_title, artist_name):
        self._song = song_title
        self._artist = artist_name
        song = self.handler.retrieve_song(song_title, artist_name)
        if song:
            raise DatabaseRoadToNowhereError(f'Song already exists: {song.title} by {song.artist.name}')

        lyrics = self.get_lyrics(song_title, artist_name)
        song, artist = self._build_song(song_title, lyrics, artist_name)
        result = SongResponseModel(artist.name, song.title, song.lyrics)

        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

        return result.as_dict

    def get_lyrics(self, song_title, artist_name):
        parsed_song = Song(title=song_title, artist=artist_name)
        self._lyrics = parsed_song.lyrics
        return parsed_song.lyrics

    def _build_artist(self, artist_name):
        artist = ArtistModel(name=artist_name)
        self.session.add(artist)
        return artist

    def _build_song(self, song_title, song_lyrics, artist_name):
        artist = self.handler.retrieve_artist(artist_name)

        if not artist:
            artist = self._build_artist(artist_name)

        song = SongModel(title=song_title, lyrics=song_lyrics, artist=artist)
        self.session.add(song)
        return song, artist


class SongHandler:
    def __init__(self, session=None):
        if session:
            self.session = session
        else:
            self.session = db.session()

    def query(self, model):
        return self.session.query(model)

    def _retrieve_all_songs(self):
        return self.query(SongModel).all()

    def _retrieve_all_artists(self):
        return self.query(ArtistModel).all()

    def retrieve_song(self, song_title, artist_name):
        return self.query(SongModel).join(ArtistModel, SongModel.artist_id == ArtistModel.id) \
            .filter(ArtistModel.name == artist_name, SongModel.title == song_title).first()

    def retrieve_artist(self, artist_name):
        return self.query(ArtistModel).filter(
            ArtistModel.name == artist_name,
        ).first()

    def get_song(self, song_title, artist_name):
        song = self.retrieve_song(song_title, artist_name)

        if song is None:
            raise DatabaseRoadToNowhereError(f'No song found: {song_title} by {artist_name}')

        return SongResponseModel(song.title, song.artist.name, song.lyrics).as_dict

    def get_all_songs(self):
        all_songs = self._retrieve_all_songs()
        results = []
        for song in all_songs:
            results.append(SongResponseModel(song.title, song.artist.name, song.lyrics))
        return MultipleSongsResponseModel(results).as_dict

    def delete_song(self, song_title, artist_name):

        artist = self.retrieve_artist(artist_name)

        if artist is None:
            raise DatabaseRoadToNowhereError(f'No artist found:  {artist_name}')

        song = self.retrieve_song(song_title, artist.name)

        if song is None:
            raise DatabaseRoadToNowhereError(f'Song was not found: {song_title} by {artist_name}')

        self.session.delete(song)

        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

        return True

    def get_random_lyrics(self):

        all_songs = self._retrieve_all_songs()

        if not all_songs:
            raise RoadToNowhereError('No songs found')

        song_count = len(all_songs)
        random_choice = random.randint(0, song_count - 1)

        song = all_songs[random_choice]
        lyrics = song.lyrics.split('\n\n')
        lyrics = [lyric for lyric in lyrics if lyric]

        return SongResponseModel(song.title, song.artist.name, random.choice(lyrics)).as_dict

    def get_all_artists(self):
        artists = self._retrieve_all_artists()
        all_artists = []

        for artist in artists:
            songs = []
            for song in artist.songs:
                songs.append(SongResponseModel(song.title, song.artist.name, song.lyrics))
            all_artists.append(ArtistResponseModel(artist.name, songs))
        return MultipleArtistsResponseModel(all_artists).as_dict
