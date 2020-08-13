import os
from typing import Iterable, Tuple
from recommender.domain.msd.sets import MSDDataReader
from recommender.domain.msd.models import Triplet, User, Song


class MSDFilesReader(MSDDataReader):

    triplets_filepath: str
    users_filepath: str
    songs_filepath: str

    def __init__(
        self,
        triplets_filepath: str,
        users_filepath: str,
        songs_filepath: str
    ):
        self.triplets_filepath = triplets_filepath
        self.users_filepath = users_filepath
        self.songs_filepath = songs_filepath

    def read_triplets(self) -> Iterable[Tuple[str, str, int]]:
        i = 0
        with open(self.triplets_filepath, "r") as f:
            for line in f:
                userid, songid, count = line.strip().split("\t")
                yield userid, songid, int(count)

    def read_users(self) -> Iterable[str]:
        with open(self.users_filepath, "r") as f:
            return [userid.strip() for userid in f.readlines()]

    def read_songs(self) -> Iterable[Tuple[str, int]]:
        with open(self.songs_filepath, "r") as f:
            for id_and_index in f.readlines():
                song_id, song_index = id_and_index.strip().split(" ")
                yield song_id, int(song_index)
