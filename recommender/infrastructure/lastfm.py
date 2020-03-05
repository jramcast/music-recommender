import logging
from datetime import datetime
from time import sleep
from recommender.domain.artist import Artist
import pylast
from typing import Iterable, List
from ..domain.track import Track


class LastFMListeningRepository:

    logger: logging.Logger

    def __init__(
        self, logger: logging.Logger, apikey, apisecret, username, password
    ) -> None:
        self.logger = logger
        self.lastfm = pylast.LastFMNetwork(
            api_key=apikey,
            api_secret=apisecret
        )
        self.username = username

    def get_tracks(
        self, time_from: datetime, time_to: datetime, retry=0
    ) -> Iterable[Track]:
        user = self.lastfm.get_user(self.username)
        try:
            rawtracks: List[pylast.PlayedTrack] = user.get_recent_tracks(
                limit=None,
                time_from=int(time_from.timestamp()),
                time_to=int(time_to.timestamp()),
            )
        except pylast.WSError as e:
            next_retry = retry + 1
            delay = next_retry**2
            self.logger.warn(f"{e}. Next try in {delay} seconds")
            sleep(delay)
            return self.get_tracks(time_from, time_to, next_retry)
        for t in rawtracks:
            # So that we don't hit the Lastfm api limits
            sleep(1)
            try:
                yield self.as_track(t)
            except Exception as e:
                self.logger.warn(f"Could not retrieve track {e}")

    def as_track(self, raw: pylast.PlayedTrack) -> Track:
        raw_artist: pylast.Artist = raw.track.artist
        raw_track: pylast.Track = raw.track
        raw_tags: List[pylast.TopItem] = raw_track.get_top_tags(limit=10)

        # to be able to retrieve user counts
        raw_track.username = self.username

        artist = Artist(
            raw_artist.get_correction() or "",
            raw_artist.get_mbid(),
        )

        if raw.timestamp:
            played_at = datetime.utcfromtimestamp(int(raw.timestamp))
        else:
            played_at = None

        return Track(
            artist,
            raw_track.get_correction() or "",
            [t.item.get_name() for t in raw_tags],
            raw_track.get_userloved() or False,
            int(raw_track.get_userplaycount() or 0),
            int(raw_track.get_playcount()),
            played_at,
            raw_track.get_mbid()
        )
