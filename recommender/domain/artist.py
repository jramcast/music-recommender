from dataclasses import dataclass


@dataclass
class Artist:
    # MusicBrainz ID
    mbid: str
    name: str
