from recommender.domain.artist import Artist
import spotipy
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import util
from typing import Iterable, List
from ..domain.track import Track


class SpotifyListeningRepository:

    spotify: spotipy.Spotify

    def __init__(self, apikey, apisecret) -> None:
        token = util.prompt_for_user_token(
                "jimmydj2000",
                scope="user-library-read",
                client_id=apikey,
                client_secret=apisecret,
                redirect_uri='http://localhost/callback'
        )
        # token = credentials.get_access_token()
        self.spotify = spotipy.Spotify(auth=token)

    def get_tracks(self) -> Iterable[Track]:
        print(self.spotify.current_user_saved_tracks())
        return []

