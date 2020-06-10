import os
import sys
import logging
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
         "../../../.."
    )
)


from recommender.infrastructure.spotify import SpotifyService


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

my_tracks = spotify.get_user_tracks()


for track in my_tracks:

    artists = " & ".join([artist["name"] for artist in track["artists"]])
    name = track["name"]
    print(f"{artists} - { name }")


# TODO: generate recommended tracks
tracks = [my_tracks[0]["id"]]


spotify.create_playlist(tracks)
