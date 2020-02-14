from typing import Optional
from dataclasses import dataclass


@dataclass
class Artist:
    # MusicBrainz ID
    name: str
    mbid: Optional[str]
