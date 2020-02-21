import csv
from recommender.domain.track import Track


class CSVTracksRepository:

    csvwriter: csv.DictWriter
    fieldnames = ["track_mbid", "track_name", "artist_mbid", "artist_name"]

    def __init__(self, filepath: str) -> None:
        csvfile = open(filepath, "w")
        self.csvwriter = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
        self.csvwriter.writeheader()

    def save(self, track: Track):
        self.csvwriter.writerow({
            "track_mbid": track.mbid,
            "track_name": track.name,
            "artist_mbid": track.artist.mbid,
            "artist_name": track.artist.name
        })
