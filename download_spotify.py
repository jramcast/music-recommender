#!/usr/bin/env python

import os
import logging
from os import environ
from pymongo import MongoClient
from recommender.infrastructure.spotify import SpotifyService
from recommender.infrastructure.repository.mongodb import MongoDBTracksRepository


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO"))
)


spotify = SpotifyService(
    logging.getLogger(),
    os.environ["SPOTIPY_USERNAME"],
    os.environ["SPOTIPY_CLIENT_ID"],
    os.environ["SPOTIPY_CLIENT_SECRET"],
    os.environ["SPOTIPY_REDIRECT_URL"]
)

client = MongoClient()
db = client.mgr
tracks_repository = MongoDBTracksRepository(db.playedtracks)


if __name__ == "__main__":

    for playedtrack in tracks_repository.all():
        spotify.get_audio_features(playedtrack)
        break
