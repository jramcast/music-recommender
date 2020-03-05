import logging
from recommender.domain.audio import SpotifyAudioFeatures
from typing import Optional
import spotipy

from spotipy import util
from ..domain.track import Track


class SpotifyService:

    spotify: spotipy.Spotify
    logger: logging.Logger

    def __init__(
        self,
        logger: logging.Logger,
        username: str,
        apikey: str,
        apisecret: str,
        redirect_uri: str
    ) -> None:
        self.logger = logger
        token = util.prompt_for_user_token(
            username,
            scope="user-library-read",
            client_id=apikey,
            client_secret=apisecret,
            redirect_uri=redirect_uri
        )
        # token = credentials.get_access_token()
        self.spotify = spotipy.Spotify(auth=token)

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
