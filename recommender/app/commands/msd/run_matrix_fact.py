"""
Matrix factorization example
"""

# Inspiration: Music Recommendations with Collaborative Filtering and Cosine Distance
# https://beckernick.github.io/music_recommender/
# 
# Inspiration: Matrix Factorization for Movie Recommendations in Python
# https://beckernick.github.io/matrix-factorization-recommender/
#
# Example Kaggle notebook:
# https://www.kaggle.com/jramcast/million-song-recommendation-engines/edit


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
user_song_plays_filepath = os.path.join(
    data_path, "TasteProfileDataset/train_triplets.txt"
)
csc_filepath = os.path.join(
    data_path, "csc_matrix.npz"
)
songs_to_index_filepath = os.path.join(
    data_path, "songs_to_index.json"
)
users_to_index_filepath = os.path.join(
    data_path, "users_to_index.json"
)



def load_taste_dataset_as_csc_matrix():
    try:
        return load_npz(csc_filepath)
    except:
        return generate_csc_matrix()


def generate_csc_matrix():

    print("Building songs count...")

    users_to_songs = {}
    song_ids = set()

    with open(user_song_plays_filepath, "r") as f:
        line = f.readline()
        while line:
            user, song, count = line.strip().split("\t")

            count = int(count)

            song_ids.add(song)

            if user in users_to_songs:
                # No user-song duplicates
                # if song in users_to_songs[user]:
                #     users_to_songs[user][song] += count
                # else:
                #     users_to_songs[user][song] = count
                users_to_songs[user][song] = count
            else:
                users_to_songs[user] = { song: count }

            line = f.readline()

    # Map songids to indexes
    with open(songs_to_index_filepath, 'w') as outfile:
        songs_to_index = { song: i for i, song in enumerate(song_ids) }
        json.dump(songs_to_index, outfile, separators=(',', ':'))

    # Map user ids to indexes
    with open(users_to_index_filepath, 'w') as outfile:
        users_to_index = { user: i for i, user in enumerate(users_to_songs.keys()) }
        json.dump(users_to_index, outfile, separators=(',', ':'))


    # Build co-ocurrence matrix
    print("Building users to songs matrix...")

    data_user_indexes = []
    data_song_indexes = []
    data = []

    for user_index, user in enumerate(users_to_songs.keys()):

        for song in users_to_songs[user].keys():

            play_count = users_to_songs[user][song]
            song_index = songs_to_index[song]

            data.append(play_count)
            data_user_indexes.append(user_index)
            data_song_indexes.append(song_index)

    data = np.array(data)
    data_user_indexes = np.array(data_user_indexes)
    data_song_indexes = np.array(data_song_indexes)

    ## Generate co-ocurrence matrix
    data = csc_matrix((data, (data_user_indexes, data_song_indexes)))

    # Persist data
    save_npz(csc_filepath, data)

    return data 

try:
    with open(users_to_index_filepath) as json_file:
        users_to_index = json.load(json_file)
except:
    generate_csc_matrix()
    with open(users_to_index_filepath) as json_file:
        users_to_index = json.load(json_file)

try:
    with open(songs_to_index_filepath) as json_file:
        songs_to_index = json.load(json_file)
except:
    generate_csc_matrix()
    with open(songs_to_index_filepath) as json_file:
        songs_to_index = json.load(json_file)


def predict(userid, songid):
    user_idx = users_to_index[userid]
    song_idx = songs_to_index[songid]

    return np.dot(W[user_idx], S[:, song_idx])
    

# Load data
X = load_taste_dataset_as_csc_matrix()
print("Loaded data")


# TODO: Normalize user listenings count: song count / total user counts


# Run matrix factorization
print("Training.. ")
model = TruncatedSVD(n_components=500, random_state=42)
W = model.fit_transform(X)
S = model.components_

# Predict example
print(
    predict("b80344d063b5ccb3212f76538f3d9e43d87dca9e", "SOIZAZL12A6701C53B")
)



