

from dataclasses import dataclass
from typing import Any, List


# Only in python 3.8
# class SpotifyAnalysis(TypedDict):
#     track: List
#     bars: List
#     beats: List
#     tatums: List
#     sections: List
#     segments: List


@dataclass
class SpotifyAudioFeatures:
    track_name: str
    track_artist: str
    features: List
    analysis: Any
