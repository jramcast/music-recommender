import pandas as pd
from recommender.domain.track import Track


class CSVTracksRepository:

    filepath: str
    columns = [
        "playback_utc_date",
        "artist_name",
        "track_name",
        "track_mbid",
        "artist_mbid",
        "user_loved",
        "user_playcount",
        "total_playcount",
        "tags"
    ]

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def all(self):
        pass

    def save(self, track: Track):
        tracks = pd.read_csv(
            self.filepath,
            # columns=self.columns,
            index_col=["playback_utc_date", "artist_name", "track_name"],
            parse_dates=["playback_utc_date"]
        )

        if tracks.empty:
            tracks = pd.DataFrame(
                track,
                columns=self.columns,
                index=["playback_utc_date", "artist_name", "track_name"])

        existing_track = tracks[
            (tracks["artist_name"] == track.artist.name) &
            (tracks["track_name"] == track.name) &
            (tracks["playback_utc_date"] == track.playback_utc_date)
        ]

        if not existing_track.empty:
            raise Exception(
                f"Track playback already exists - " +
                f"{track.artist.name} {track.name} {track.playback_utc_date}"
            )

        tracks.append(track)

        tracks.to_csv(
            self.filepath,
            mode="a",
            header=is_empty,
            index=False
        )
