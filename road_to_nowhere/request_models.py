from dataclasses import dataclass


@dataclass
class SongRequestModel:
    song: str
    artist: str
