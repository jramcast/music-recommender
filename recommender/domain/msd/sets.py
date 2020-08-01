from abc import ABC
from recommender.domain.msd.models import Song, Triplet, User
from typing import Dict, Iterable, Set



class MSDDataReader(ABC):

    def read_taste_triplets(self) -> Iterable[Triplet]:
        raise NotImplementedError()

    def read_kaggle_users(self) -> Dict[str, int]:
        raise NotImplementedError()

    def read_kaggle_songs(self) -> Dict[str, int]:
        raise NotImplementedError()



class UserListens:

    users = set()
    songs = set()
    reader: MSDDataReader
    songs_by_user: Dict[User, Set[Song]] = {}

    def __init__(self, reader: MSDDataReader) -> None:
        self.reader = reader

    def load(self):
        for triplet in self.reader.read_taste_triplets():
            user = triplet.user
            song = triplet.song

            self.users.add(user)
            self.songs.add(song)

            if user in self.songs_by_user:
                self.songs_by_user[user].add(song)
            else:
                self.songs_by_user[user] = set([song])

    def get_user_songs(self, user: User):
        return self.songs_by_user[user]

    def user_has_listened_to(self, user: User, song: Song):
        return song in self.songs_by_user[user]
