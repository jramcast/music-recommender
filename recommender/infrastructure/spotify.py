import logging
from recommender.domain.audio import SpotifyAudioFeatures
from typing import Iterable, Optional
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

        try:
            search_results = self.spotify.search(
                f"artist:{track_artist} track:{track_name}",
                limit=1
            )
        except spotipy.client.SpotifyException as e:
            if e.http_status == 401:
                self._login()
                search_results = self.spotify.search(
                    f"artist:{track_artist} track:{track_name}",
                    limit=1
                )
            else:
                raise e

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
                if e.http_status == 401:
                    self._login()
                    return self.get_audio_features(track)
                elif e.http_status == 404:
                    self.logger.warn(
                        f"Audio features not found for " +
                        f"{track_artist} - {track_name}"
                    )
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

    def get_user_tracks(self, limit=20, offset=0) -> Iterable:
        response =  self.spotify.current_user_saved_tracks(limit, offset)
        return [item["track"] for item in response["items"]]

    def create_playlist(self, tracks=[]):
        playlist_id = ""
        
        response = self.spotify.user_playlists(self.username)

        for playlist in response["items"]:
            if playlist["name"] == "Test playlist":
                playlist_id = playlist["id"]
                break

        
        self.spotify.user_playlist_add_tracks(self.username, playlist_id, tracks)

    def _login(self):
        token = util.prompt_for_user_token(
            self.username,
            scope="playlist-modify-public,user-library-read",
            client_id=self.apikey,
            client_secret=self.apisecret,
            redirect_uri=self.redirect_uri
        )
        # token = credentials.get_access_token()
        self.spotify = spotipy.Spotify(auth=token)