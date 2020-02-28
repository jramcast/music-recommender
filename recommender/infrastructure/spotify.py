import logging
import spotipy

from spotipy import util
from ..domain.track import Track
import json


class SpotifyService:

    spotify: spotipy.Spotify

    def __init__(
        self,
        logger: logging.Logger,
        username: str,
        apikey: str,
        apisecret: str,
        redirect_uri: str
    ) -> None:
        token = util.prompt_for_user_token(
                username,
                scope="user-library-read",
                client_id=apikey,
                client_secret=apisecret,
                redirect_uri=redirect_uri
        )
        # token = credentials.get_access_token()
        self.spotify = spotipy.Spotify(auth=token)

    def get_audio_features(self, track: Track):
        print(track)
        search_results = self.spotify.search(
            f"artist:{track.artist.name} track:{track.name}", limit=1
        )
        search_items = search_results["tracks"]["items"]
        if len(search_items) > 0:
            spotify_track = search_items[0]
            audio_features = self.spotify.audio_features(spotify_track["id"])
            print(json.dumps(audio_features))
            audio_analysis = self.spotify.audio_analysis(spotify_track["id"])
            print(json.dumps(audio_analysis))

