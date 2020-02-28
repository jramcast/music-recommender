#!/usr/bin/env python

import os
import logging
import pymongo
from datetime import datetime, timedelta
from pymongo import MongoClient
from recommender.infrastructure.lastfm import LastFMListeningRepository
from recommender.infrastructure.repository.mongodb import MongoDBTracksRepository

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO"))
)

listening_repo = LastFMListeningRepository(
    logging.getLogger(),
    os.environ["LASTFM_API_KEY"],
    os.environ["LASTFM_API_SECRET"],
    os.environ["LASTFM_USERNAME"],
    os.environ["LASTFM_PASSWORD"],
)

client = MongoClient()
db = client.mgr
tracks_repository = MongoDBTracksRepository(db.playedtracks)


START_TIME = datetime(2007, 8, 4)
END_TIME = datetime(2020, 3, 1)


if __name__ == "__main__":

    day = START_TIME

    while day <= END_TIME:
        next_day = day + timedelta(days=1)
        tracks = listening_repo.get_tracks(time_from=day, time_to=next_day)
        day = next_day
        for t in tracks:
            logging.info(f"TRACK PLAYBACK: {t}")
            try:
                tracks_repository.save(t)
            except pymongo.errors.DuplicateKeyError as e:
                logging.warning(f"Ignoring duplicate record. {e}")
