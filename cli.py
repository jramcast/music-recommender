#!/usr/bin/env python

import os
import logging
import pickle
from recommender.infrastructure.lastfm import LastFMListeningRepository

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO"))
)


repository = LastFMListeningRepository(
    os.environ["LASTFM_API_KEY"],
    os.environ["LASTFM_API_SECRET"],
    os.environ["LASTFM_USERNAME"]
)

with open('data/tracks.csv', 'a') as datafile:
    tracks = repository.get_tracks()

    for t in tracks:
        print("track", t)
        datafile.write(str(pickle.dumps(t)) + "\n")

if __name__ == "__main__":
    print(tracks)
