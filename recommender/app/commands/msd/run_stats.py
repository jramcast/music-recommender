import os
import sys
sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../../../.."
    )
)

import pathlib
import json
import pandas as pd
import numpy as np
from timeit import default_timer as timer
from scipy.sparse import csc_matrix, save_npz, load_npz
from recommender.domain.scoring import msd_mAP
from sklearn.decomposition import TruncatedSVD


data_path = os.path.join(
    pathlib.Path(__file__).parent.absolute(),
    "../../../../data/msdchallenge/"
)

kaggle_users_filepath = os.path.join(
    data_path, "kaggle_challenge_files/kaggle_users.txt"
)

kaggle_songs_filepath = os.path.join(
    data_path, "kaggle_challenge_files/kaggle_songs.txt"
)

tfd_train_triplets_filepath = os.path.join(
    data_path, "TasteProfileDataset/train_triplets.txt"
)

eval_triplets_filepath = os.path.join(
    data_path, "kaggle_challenge_files/kaggle_visible_evaluation_triplets.txt"
)


def get_train_triplets():
    with open(tfd_train_triplets_filepath, "r") as f:
        # train_triplets = [line.strip().split("\t") for line in f] # generates [user, song, count]
        for line in f:
            yield line.strip().split("\t")


print(" === Kaggle data ===")

# Build songs list 
# (kaggle already has all songs so we only need to get them from the kaggle file)
songs_to_index = {}
songs_index_to_ids = {}
with open(kaggle_songs_filepath, "r") as f:
    for id_and_index in f.readlines():
        songid, index = id_and_index.strip().split(" ")
        index = int(index)
        songs_to_index[songid] = index
        songs_index_to_ids[index] = songid

print("Full song list (train + test): ", len(songs_to_index.keys()))


## Include kaggle users
kaggle_users = []
with open(kaggle_users_filepath, "r") as f:
    kaggle_users = [userid.strip() for userid in f.readlines()]

print("Eval Users: ", len(kaggle_users))

# Load evaluation listening histories
eval_listen_count = {}
songs_in_eval = set()
with open(eval_triplets_filepath, "r") as f:
    line = f.readline()
    while line:
        user, song, _ = line.strip().split("\t")
        songidx = songs_to_index[song]

        songs_in_eval.add(songidx)

        if user in eval_listen_count:
            eval_listen_count[user].add(songidx)
        else:
            eval_listen_count[user] = set([songidx])

        line = f.readline()

print("Songs in eval triplets: ", len(songs_in_eval))



print("=== TPF data ===")

## Tasteprofile trainig set users
training_users = set([user for user, _, _ in get_train_triplets()])

print("TPF training users from train_triplets: ", len(training_users))

print(
    "Are kaggle EVAL users and tpf TRAINING users disjoint? ", 
    set(kaggle_users).isdisjoint(set(training_users)))