#!/usr/bin/env python

import os
import json
import logging
import pylast
from pprint import pprint
from dotenv import load_dotenv


load_dotenv()


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO"))
)

network = pylast.LastFMNetwork(
    api_key=os.environ["LASTFM_API_KEY"],
    api_secret=os.environ["LASTFM_API_SECRET"],
    username=os.environ["LASTFM_USERNAME"],
    password_hash=pylast.md5(os.environ["LASTFM_PASSWORD"])
)

def get_song_tags(artist, track):
    track = network.get_track(artist, track)
    return [(tag.item.name, tag.weight) for tag in track.get_top_tags()]

if __name__ == "__main__":

    TRACKS = [
        ("Queen", "Bohemian Rhapsody"),
        ("Paco de Lucía", "Entre dos Aguas"),
        ("Sensible soccers", "AFG"),
    ]

    tags = {}
    for track in TRACKS:
        key = f"{track[0]} - {track[1]}"
        tags[key] = get_song_tags(track[0], track[1])

    with open("song_tags.json", "w") as outfile:
        json.dump(tags, outfile, indent=2)