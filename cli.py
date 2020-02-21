#!/usr/bin/env python

import os
import logging
import pickle
from recommender.infrastructure.lastfm import LastFMListeningRepository
from recommender.infrastructure.repository.csv import CSVTracksRepository

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO"))
)


lastfm = LastFMListeningRepository(
    os.environ["LASTFM_API_KEY"],
    os.environ["LASTFM_API_SECRET"],
    os.environ["LASTFM_USERNAME"]
)

tracks_repository = CSVTracksRepository("data/tracks.csv")


if __name__ == "__main__":
    tracks = lastfm.get_tracks()
    for t in tracks:
        print("track", t)
        tracks_repository.save(t)
