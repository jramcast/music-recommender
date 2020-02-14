import os
import logging
from recommender.infrastructure.lastfm import LastFMListeningRepository
from recommender.infrastructure.http.flask.server import FlaskServer

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO"))
)


app = FlaskServer().app


repository = LastFMListeningRepository(
    os.environ["LASTFM_API_KEY"],
    os.environ["LASTFM_API_SECRET"],
    os.environ["LASTFM_USERNAME"]
)

tracks = repository.get_tracks()


if __name__ == "__main__":
    print(tracks)
