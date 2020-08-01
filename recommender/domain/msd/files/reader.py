import os
from recommender.domain.msd.sets import MSDDataReader
from typing import Iterable
from recommender.domain.msd.models import Triplet, User, Song




class MSDFilesReader(MSDDataReader):

    def __init__(self, datadir):
        self.datadir = datadir


        self.kaggle_users_filepath = os.path.join(
            self.datadir, "kaggle_challenge_files/kaggle_users.txt"
        )

        self.kaggle_songs_filepath = os.path.join(
            self.datadir, "kaggle_challenge_files/kaggle_songs.txt"
        )

        self.tfd_train_triplets_filepath = os.path.join(
            self.datadir, "TasteProfileDataset/train_triplets.txt"
        )
        self.csc_filepath = os.path.join(
            self.datadir, "csc_matrix.npz"
        )
        self.songs_to_index_filepath = os.path.join(
            self.datadir, "songs_to_index.json"
        )
        self.users_to_index_filepath = os.path.join(
            self.datadir, "users_to_index.json"
        )

        self.kaggle_triplets_filepath = os.path.join(
            self.datadir, "kaggle_challenge_files/kaggle_visible_evaluation_triplets.txt"
        )

    def read_taste_triplets(self) -> Iterable[Triplet]:
        i = 0
        with open(self.tfd_train_triplets_filepath, "r") as f:
            for line in f:
                userid, songid, count = line.strip().split("\t")
                user = User(userid, 0)
                song = Song(songid, 0)
                i+=1
                if i > 100000:
                    break
                yield Triplet(user, song, int(count))

    def read_kaggle_users(self):
        with open(self.kaggle_users_filepath, "r") as f:
            return [userid.strip() for userid in f.readlines()]
            
    def read_kaggle_songs(self):
        with open(self.kaggle_songs_filepath, "r") as f:
            for id_and_index in f.readlines():
                song_id, song_index = id_and_index.strip().split(" ")
                yield song_id, int(song_index)

    

