"""
Matrix factorization example
"""

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
import pandas as pd
import numpy as np
from recommender.domain.scoring import msd_average_precision, msd_mAP

data_path = os.path.join(
    pathlib.Path(__file__).parent.absolute(),
    "../../../../data/msdchallenge/kaggle_challenge_files"
)

user_song_plays_filepath = os.path.join(
    data_path, "kaggle_visible_evaluation_triplets.txt"
)
users_filepath = os.path.join(
    data_path, "kaggle_users.txt"
)
songs_filepath = os.path.join(
    data_path, "kaggle_songs.txt"
)

# Load song popularity as song play count

users_to_songs = {}
song_ids = set()


print("Building songs count...")

with open(user_song_plays_filepath, "r") as f:
    line = f.readline()
    while line:
        user, song, _ = line.strip().split("\t")

        song_ids.add(song)

        if user in users_to_songs:
            if song in users_to_songs[user]:
                users_to_songs[user][song] += 1
            else:
                users_to_songs[user][song] = 1
        else:
            users_to_songs[user] = { song: 1 }

        line = f.readline()



print("Building users to songs matrix...")

user_ids = users_to_songs.keys()
num_users = len(user_ids)
num_songs = len(song_ids)

# for i, user in enumerate(user_ids):

#     for j, song in enumerate(song_ids):
#         data[i][j] = users_to_songs[user].get(song, 0)



matrix = pd.DataFrame(
    0,
    index=user_ids,
    columns=song_ids,
    dtype="int8"
).to_sparse(0)


print(matrix.head())

for user in user_ids:

    for song in users_to_songs[user].keys():
        matrix.at[user, song] = users_to_songs[user][song]


