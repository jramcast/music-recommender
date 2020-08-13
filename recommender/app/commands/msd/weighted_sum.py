import os
import sys
import time
import pathlib
from typing import Iterable
sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../../../.."
    )
)

import numpy as np
import progressbar

from recommender.domain.scoring import msd_mAP
from recommender.domain.msd.models import User, Song
from recommender.domain.msd.sets import UserListens
from recommender.domain.msd.files.reader import MSDFilesReader

datadir = os.path.join(
    pathlib.Path(__file__).parent.absolute(),
    "../../../../data/msdchallenge/"
)
kaggle_users_filepath = os.path.join(
    datadir, "kaggle_challenge_files/kaggle_users.txt"
)

kaggle_songs_filepath = os.path.join(
    datadir, "kaggle_challenge_files/kaggle_songs.txt"
)

tfd_train_triplets_filepath = os.path.join(
    datadir, "TasteProfileDataset/train_triplets.txt"
)
csc_filepath = os.path.join(
    datadir, "csc_matrix.npz"
)
songs_to_index_filepath = os.path.join(
    datadir, "songs_to_index.json"
)
users_to_index_filepath = os.path.join(
    datadir, "users_to_index.json"
)


training_set_reader = MSDFilesReader(
    os.path.join(datadir, "kaggle_challenge_files/kaggle_visible_evaluation_triplets.txt"),
    os.path.join(datadir, "kaggle_challenge_files/kaggle_users.txt"),
    os.path.join(datadir, "kaggle_challenge_files/kaggle_songs.txt")
)
training_set = UserListens(training_set_reader)


print("TRAINING SET: Loading listening co-ocurrences...")
training_set.load()


def score(user: User, target_song: Song):
    score = 0
    for song in training_set.get_songs():
        similarity = get_songs_similarity(target_song, song)
        score += similarity # * int(user_listens_training.user_has_listened_to(user, target_song))

    return score / len(training_set.songs) # normalize


def load_coocurrences():
    coocurrences = {}
    totals = {}

    progress = progressbar.ProgressBar(
        maxval=len(training_set.users),
        widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()]
    )

    progress.start()
    for i, user in enumerate(training_set.get_users()):
        user_songs = training_set.get_user_songs(user)

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
    if a in coocurrences:
        count = coocurrences[a].get(b, 0)
        return count / totals[a]
    
    return 0


def evaluate(data: UserListens):

    # Compute recommendations for evaluation users
    recommendations = {}

    for user in data.get_users():


        scores = np.zeros(shape=len(data.songs))

        for song in data.get_songs():
            print(song)
            scores[song.kaggle_index] = score(user, song)

        # Do not recommend already known songs
        # indexes_to_drop = list(drop.get(userid, []))
        # np.put(predictions, indexes_to_drop, 0)

        # To get a rank, we must revers the order
        # We also need to limit the rank to 500
        ranked = np.argsort(scores)[::-1][:500]

        # recommendations[userid] = [songs_index_to_ids[idx] for idx in ranked]
        recommendations[user.id] = ranked


    return msd_mAP(
        data.users,
        recommendations,
        data.songs_by_user
    )



start = time.time()

# rec_score = score(
#     User("b80344d063b5ccb3212f76538f3d9e43d87dca9e", 0), 
#     Song("SOBFOVM12A58A7D494", 0)
#     #Song("SOBVAHM12A8C13C4CB", 0)
# )

# print(f"Score: {rec_score}")


eval_set_reader = MSDFilesReader(
    os.path.join(datadir, "kaggle_challenge_files/kaggle_visible_evaluation_triplets.txt"),
    os.path.join(datadir, "kaggle_challenge_files/kaggle_users.txt"),
    os.path.join(datadir, "kaggle_challenge_files/kaggle_songs.txt")
)
user_listens_eval = UserListens(eval_set_reader)



evaluate(user_listens_eval)

end = time.time()
print(f"Elapsed time: {end - start} seconds")
