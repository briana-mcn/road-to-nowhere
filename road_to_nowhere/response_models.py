from dataclasses import asdict, dataclass
from typing import List


@dataclass
class SongResponseModel:
    artist: str = None
    title: str = None
    lyrics: str = None

    @property
    def as_dict(self):
        return asdict(self)


@dataclass
class MultipleSongsResponseModel:
    songs: List[SongResponseModel] = None

    @property
    def as_dict(self):
        return asdict(self)


@dataclass
class ArtistResponseModel:
    name: str = None
    songs: List[SongResponseModel] = None

    @property
    def as_dict(self):
        return asdict(self)


@dataclass
class MultipleArtistsResponseModel:
    artists: List[ArtistResponseModel] = None

    @property
    def as_dict(self):
        return asdict(self)
