#!/usr/bin/env python

import os
import logging
from time import sleep
from dotenv import load_dotenv
from pymongo import MongoClient
from recommender.infrastructure.spotify import SpotifyService
from recommender.infrastructure.repository.mongodb import (
    MongoDBSpotifyAudioFeaturesRepository, MongoDBTracksRepository)


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO"))
)

load_dotenv()

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
audio_features_repository = MongoDBSpotifyAudioFeaturesRepository(
    db.spotify_audiofeatures
)


if __name__ == "__main__":

    count = 0

    for track in tracks_repository.all():

        logging.info(f"Processed {count}")
        count += 1
        # if count < 45900:
        #     continue

        if audio_features_repository.load(track):
            logging.info(f"Skipping {track} features already in DB.")
            continue

        features = spotify.get_audio_features(track)
        if features:
            audio_features_repository.save(features)
            logging.info(f"Got audio features for {track}")

        sleep(1)
