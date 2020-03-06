#!/usr/bin/env python

from typing import Counter
from pymongo import MongoClient
from recommender.infrastructure.repository.mongodb import (
    MongoDBTracksRepository
)

client = MongoClient()
db = client.mgr
tracks_repository = MongoDBTracksRepository(db.playedtracks)


if __name__ == "__main__":

    tags_by_hour = {}

    for track in tracks_repository.all():
        if track.tags:
            hour = track.playback_utc_date.hour
            tags = tags_by_hour.get(hour, []) + track.tags
            tags_by_hour[hour] = tags

    hour = 12

    tags_counter = Counter(tags_by_hour[hour])

    track_scores = {}
    for track in tracks_repository.all():
        track_score = 0
        for (tag, tag_count) in tags_counter.most_common():
            if tag in track.tags:
                track_score += tag_count

        track_scores[f"{track.artist.name}__{track.name}"] = track_score

    results = []

    for track_key, score in track_scores.items():
        results.append((track_key, score))

    results.sort(key=lambda x: -x[1])

    for recommendation in results[:10]:
        print(recommendation)






