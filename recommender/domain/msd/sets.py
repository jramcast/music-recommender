from abc import ABC
from recommender.domain.msd.models import Song, Triplet, User
from typing import Dict, Iterable, List, Set, Tuple


class MSDDataReader(ABC):

    def read_triplets(self) -> Iterable[Tuple[str, str, int]]:
        raise NotImplementedError()

    def read_users(self) -> Iterable[str]:
        raise NotImplementedError()

    def read_songs(self) -> Iterable[Tuple[str, int]]:
        raise NotImplementedError()


class UserListens:

    users: Dict[str, User] = {}
    songs: Dict[str, Song] = {}
    reader: MSDDataReader
    songs_by_user: Dict[User, Set[Song]] = {}

    def __init__(self, reader: MSDDataReader):
        self.reader = reader

    def load(self):

        for userid in self.reader.read_users():
            self.users[userid] = User(userid) 
    
        for songid, kaggle_index in self.reader.read_songs():
            self.songs[songid] = Song(songid, kaggle_index) 

        i = 0

        for userid, songid, count in self.reader.read_triplets():

            user = self.users[userid]
            song = self.songs[songid]
            
            triplet =  Triplet(user, song, count)

            if user in self.songs_by_user:
                self.songs_by_user[user].add(song)
            else:
                self.songs_by_user[user] = set([song])

            i += 1
            if i > 100:
                break

    def get_users(self) -> Iterable[User]:
        return self.users.values()

    def get_songs(self) -> Iterable[Song]:
        return self.songs.values()

    def get_user_songs(self, user: User):
        return self.songs_by_user.get(user, [])

    def user_has_listened_to(self, user: User, song: Song):
        return song in self.songs_by_user[user]
