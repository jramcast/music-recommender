import logging
from recommender.domain.audio import SpotifyAudioFeatures
from typing import Optional
import spotipy

from spotipy import util
from ..domain.track import Track


class SpotifyService:

    spotify: spotipy.Spotify
    logger: logging.Logger
    username: str
    apikey: str
    apisecret: str
    redirect_uri: str

    def __init__(
        self,
        logger: logging.Logger,
        username: str,
        apikey: str,
        apisecret: str,
        redirect_uri: str
    ) -> None:
        self.logger = logger
        self.username = username
        self.apikey = apikey
        self.apisecret = apisecret
        self.redirect_uri = redirect_uri
        self._login()

    def get_audio_features(
        self, track: Track
    ) -> Optional[SpotifyAudioFeatures]:

        track_name = track.name
        track_artist = track.artist.name

        search_results = self.spotify.search(
            f"artist:{track_artist} track:{track_name}",
            limit=1
        )
        search_items = search_results["tracks"]["items"]

        if len(search_items) > 0:
            spotify_track = search_items[0]
            try:
                audio_features = self.spotify.audio_features(
                    spotify_track["id"]
                )
                audio_analysis = self.spotify.audio_analysis(
                    spotify_track["id"]
                )

                return SpotifyAudioFeatures(
                    track_name,
                    track_artist,
                    audio_features,
                    audio_analysis
                )
            except spotipy.client.SpotifyException as e:
                if "expired" in e.msg:
                    self._login()
                    return self.get_audio_features(track)
                else:
                    raise e

            except Exception as e:
                self.logger.warn(
                    f"Error while getting audio features for " +
                    f"{track_artist} - {track_name}. Error {e}"
                )
        else:
            self.logger.warn(
                f"No audio features available for " +
                f"{track_artist} - {track_name}"
            )
            return None

    def _login(self):
        token = util.prompt_for_user_token(
            self.username,
            scope="user-library-read",
            client_id=self.apikey,
            client_secret=self.apisecret,
            redirect_uri=self.redirect_uri
        )
        # token = credentials.get_access_token()
        self.spotify = spotipy.Spotify(auth=token)