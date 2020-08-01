from dataclasses import dataclass

@dataclass
class User:
    id: str
    kaggle_index: int

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

@dataclass
class Song:
    id: str
    kaggle_index: int

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

@dataclass
class Triplet:
    user: User
    song: Song
    count: int
