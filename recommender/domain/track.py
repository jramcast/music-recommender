from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass
from .artist import Artist


@dataclass
class Track:
    artist: Artist
    name: str
    tags: List[str]
    loved: bool
    user_playcount: int
    total_playcount: int
    playback_utc_date: Optional[datetime]
    mbid: Optional[str] = None

    def __repr__(self) -> str:
        return f"{self.artist.name} - '{self.name}' at '{self.playback_utc_date}'"
