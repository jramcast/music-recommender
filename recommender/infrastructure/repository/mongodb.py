from dataclasses import asdict
from typing import Iterable
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

    def all(self) -> Iterable[Track]:
        for doc in self.collection.find():
            yield self._as_track(doc)

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
