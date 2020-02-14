from dataclasses import dataclass
from .artist import Artist


@dataclass
class Track:
    artist: Artist
    name: str
