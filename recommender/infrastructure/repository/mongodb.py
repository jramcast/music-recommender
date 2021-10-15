from dataclasses import asdict
from recommender.domain.audio import SpotifyAudioFeatures
from typing import Iterable, Optional
import pymongo
from recommender.domain.track import Track
from recommender.domain.artist import Artist


class MongoDBTracksRepository:

    collection: pymongo.collection.Collection

    def __init__(self, collection: pymongo.collection.Collection):
        self.collection = collection
        self.collection.create_index(
            [
                ("playback_utc_date", pymongo.ASCENDING),
                ("name", pymongo.ASCENDING),
                ("artist.name", pymongo.ASCENDING)
            ],
            unique=True
        )

    def all(self, recent_first=True) -> Iterable[Track]:
        for doc in self.all_raw(recent_first):
            yield self._as_track(doc)

    def all_raw(self, recentFirst=False) -> Iterable[any]:
        return (self.collection
                    .find()
                    .sort("playback_utc_date", 1 if not recentFirst else -1))

    def save(self, track: Track):
        self.collection.insert_one(asdict(track))

    def _as_track(self, doc) -> Track:

        artist = Artist(
            doc["artist"]["name"],
            doc["artist"]["mbid"]
        )

        return Track(
            artist,
            doc["name"],
            doc["tags"],
            doc["loved"],
            doc["user_playcount"],
            doc["total_playcount"],
            doc["playback_utc_date"],
            doc["mbid"]
        )


class MongoDBSpotifyAudioFeaturesRepository:

    collection: pymongo.collection.Collection

    def __init__(self, collection: pymongo.collection.Collection):
        self.collection = collection
        self.collection.create_index(
            [
                ("track_name", pymongo.ASCENDING),
                ("track_artist", pymongo.ASCENDING)
            ],
            unique=True
        )

    def load(self, track: Track) -> Optional[SpotifyAudioFeatures]:
        return self.collection.find_one({
            "track_name": track.name,
            "track_artist": track.artist.name
        })

    def all(self) -> Iterable[SpotifyAudioFeatures]:
        for doc in self.collection.find():
            yield self._as_audio_features(doc)

    def save(self, features: SpotifyAudioFeatures):
        self.collection.insert_one(asdict(features))

    def _as_audio_features(self, doc) -> SpotifyAudioFeatures:

        return SpotifyAudioFeatures(
            doc["track_name"],
            doc["track_artist"],
            doc["features"],
            doc["analysis"],
        )
