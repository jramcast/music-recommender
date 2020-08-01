import os
import sys
import time
import pathlib
sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../../../.."
    )
)

import progressbar

from recommender.domain.msd.models import User, Song
from recommender.domain.msd.sets import UserListens
from recommender.domain.msd.files.reader import MSDFilesReader

datadir = os.path.join(
    pathlib.Path(__file__).parent.absolute(),
    "../../../../data/msdchallenge/"
)



datareader = MSDFilesReader(datadir)
user_listens = UserListens(datareader)

print("Loading listening co-ocurrences...")
user_listens.load()


def score(user, target_song):
    score = 0
    for song in user_listens.songs:
        similarity = get_songs_similarity(target_song, song)
        score += similarity # * int(user_listens.user_has_listened_to(user, target_song))

    return score / len(user_listens.songs) # normalize


def load_coocurrences():
    coocurrences = {}
    totals = {}

    progress = progressbar.ProgressBar(
        maxval=len(user_listens.users),
        widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()]
    )

    progress.start()
    for i, user in enumerate(user_listens.users):
        user_songs = user_listens.get_user_songs(user)

        for song in user_songs:
            totals[song] = 1 + totals.get(song, 0)

            if song not in coocurrences:
                coocurrences[song] = {}

            other_user_songs = user_songs - set([song])

            for other_song in other_user_songs:
                coocurrences[song][other_song] = 1 + coocurrences[song].get(other_song, 0)

        progress.update(i+1)
    
    progress.finish()
    return coocurrences, totals


coocurrences, totals = load_coocurrences()


def get_songs_similarity(a: Song, b: Song):
    
    count = coocurrences[a].get(b, 0)

    print("a U b", count)
    print("a", totals[a])
    print("----")

    return count / totals[a]


start = time.time()

rec_score = score(
    User("b80344d063b5ccb3212f76538f3d9e43d87dca9e", 0), 
    Song("SOBFOVM12A58A7D494", 0)
    #Song("SOBVAHM12A8C13C4CB", 0)
)

print(f"Score: {rec_score}")

end = time.time()
print(f"Elapsed time: {end - start} seconds")
