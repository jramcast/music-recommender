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
from scipy.sparse import csc_matrix, save_npz, load_npz
from recommender.domain.scoring import msd_average_precision, msd_mAP
from sklearn.decomposition import TruncatedSVD


data_path = os.path.join(
    pathlib.Path(__file__).parent.absolute(),
    "../../../../data/msdchallenge/"
)

print("Reading triplets...")

tfd_train_triplets_filepath = os.path.join(
    data_path, "TasteProfileDataset/train_triplets.txt"
)

def get_train_triplets():
    with open(tfd_train_triplets_filepath, "r") as f:
        # train_triplets = [line.strip().split("\t") for line in f] # generates [user, song, count]
        for line in f:
            yield line.strip().split("\t")



kaggle_users_filepath = os.path.join(
    data_path, "kaggle_challenge_files/kaggle_users.txt"
)

# Build users list

print("Building users list...")

# Include kaggle users
users = []
with open(kaggle_users_filepath, "r") as f:
    users = [userid.strip() for userid in f.readlines()]

# An also users from train triplets
users = set(users +  [user for user, _, _ in get_train_triplets()])

users_to_index = dict([(userid, idx) for (idx, userid) in enumerate(users)])


print("Building songs list...")

# Build songs list (kaggle already has all songs so we only need to get them from there)

kaggle_songs_filepath = os.path.join(
    data_path, "kaggle_challenge_files/kaggle_songs.txt"
)
songs_to_index = {}
with open(kaggle_songs_filepath, "r") as f:
    songs_to_index = dict(
        [id_and_index.strip().split(" ") for id_and_index in f.readlines()]
    )


users_to_songs = {}
song_ids = set()


print("Processing listening counts...")

for user, song, count in get_train_triplets():
    count = int(count)

    song_ids.add(song)

    if song not in songs_to_index:
        print("song " + song + " not in song_to_idex")

    if user in users_to_songs:
        # No user-song duplicates
        # if song in users_to_songs[user]:
        #     users_to_songs[user][song] += count
        # else:
        #     users_to_songs[user][song] = count
        users_to_songs[user][song] = count
    else:
        users_to_songs[user] = { song: count }



# Build co-ocurrence matrix
print("Building users to songs matrix...")

data_user_indexes = []
data_song_indexes = []
data = []

for user in users_to_index.keys():

    user_index = int(users_to_index[user])

    for songid in users_to_songs.get(user, {}).keys():

        play_count = users_to_songs[user][songid]
        song_index = int(songs_to_index[songid])

        data.append(play_count)
        data_user_indexes.append(user_index)
        data_song_indexes.append(song_index)

data = np.array(data)
data_user_indexes = np.array(data_user_indexes)
data_song_indexes = np.array(data_song_indexes)

print(data.shape)
print(data_user_indexes.shape)
print(data_song_indexes.shape)


## Generate co-ocurrence matrix
data = csc_matrix((data, (data_user_indexes, data_song_indexes)))

print(data)