#!/usr/bin/env python


"""
Recommender basic test
based on cosine similarity between vectors of "preferences" and recommended songs
"""

import os
import sys
sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../../.."
    )
)

import numpy as np
from typing import Counter, List
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient
from recommender.domain.track import Track
from recommender.infrastructure.repository.mongodb import (
    MongoDBTracksRepository
)

client = MongoClient()
db = client.mgr
tracks_repository = MongoDBTracksRepository(db.playedtracks)


LABELS = []


def extract_track_features(track: Track):
    tags = [tag.lower() for tag in track.tags]
    features = []
    for i in range(5):
        if i < len(tags):
            features.append(tags[i])
        else:
            features.append(None)
    return features


def is_track_relevant(track: Track):
    return track.tags and (track.loved or track.user_playcount >= -1)


def calculate_max_similarity(track: Track, preferences: List[List[str]]):
    track_features = []
    for label in LABELS:
        if label in track.tags:
            track_features.append(1)
        else:
            track_features.append(0)

    a = np.array(track_features).reshape(1, len(LABELS))
    b = np.array(preferences)

    similarity_to_prefence_vectors = cosine_similarity(a, b)
    return np.max(similarity_to_prefence_vectors)


def str_to_bytes(x):
    return np.array([ord(c) for c in x])


def preprocess_preferences(preferences):
    for row in preferences:
        for feature in row:
            if feature not in LABELS:
                LABELS.append(feature)

    preprocessed_preferences = []
    for row in preferences:
        preprocessed_row = []
        for label in LABELS:
            if label in row:
                preprocessed_row.append(1)
            else:
                preprocessed_row.append(0)

        preprocessed_preferences.append(preprocessed_row)

    return preprocessed_preferences


def sort_rank_fn(each):
    return -each[1]


if __name__ == "__main__":

    preferences = []

    train_songs = tracks_repository.all()

    for track in train_songs:
        if is_track_relevant(track):
            preferences.append(extract_track_features(track))

    preprocessed_preferences = preprocess_preferences(preferences)

    rank = []
    # Todo: get a test set
    test_songs = list(tracks_repository.all())[:-10]
    for t in test_songs:
        similarity = calculate_max_similarity(t, preprocessed_preferences)
        rank.append((t, similarity))

    print(sorted(rank, key=sort_rank_fn))
