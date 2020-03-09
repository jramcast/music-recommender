#!/usr/bin/env python


"""
Recommender basic test
based on
https://www.mendeley.com/viewer/?fileId=20d7cbe3-573e-fc75-63c3-8e1f174869a8&documentId=28288f63-525b-3f5d-a309-a7d1b9281c25
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

    return cosine_similarity([track_features], preferences)


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
        for i, label in enumerate(LABELS):
            if label in track.tags:
                preprocessed_row.append(1)
            else:
                preprocessed_row.append(0)

        preprocessed_preferences.append(preprocessed_row)

    return preprocessed_preferences


if __name__ == "__main__":

    preferences = []

    for track in tracks_repository.all():
        if is_track_relevant(track):
            preferences.append(extract_track_features(track))

    print(calculate_max_similarity(
        list(tracks_repository.all())[35],
        preprocess_preferences(preferences)
    ))