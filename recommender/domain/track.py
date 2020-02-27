from typing import Optional, List
from dataclasses import dataclass
from .artist import Artist


@dataclass
class Track:
    artist: Artist
    name: str
    user_playcount: int
    total_playcount: int
    tags: List[str]
    mbid: Optional[str] = None
