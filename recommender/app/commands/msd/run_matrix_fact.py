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
#
# Utils:
# https://gist.github.com/tgsmith61591/ce7d614d7a0442f94cd5ae5d1e51d3c2
# https://towardsdatascience.com/how-to-use-cross-validation-for-matrix-completion-2b14103d2c4c
 

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
from recommender.domain.scoring import msd_average_precision, msd_mAP
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
csc_filepath = os.path.join(
    data_path, "csc_matrix.npz"
)
songs_to_index_filepath = os.path.join(
    data_path, "songs_to_index.json"
)
users_to_index_filepath = os.path.join(
    data_path, "users_to_index.json"
)

eval_triplets_filepath = os.path.join(
    data_path, "kaggle_challenge_files/kaggle_visible_evaluation_triplets.txt"
)


def get_train_triplets():
    with open(tfd_train_triplets_filepath, "r") as f:
        # train_triplets = [line.strip().split("\t") for line in f] # generates [user, song, count]
        for line in f:
            yield line.strip().split("\t")


# Build users list

print("Building users list...")

## Include kaggle users
users = []
with open(kaggle_users_filepath, "r") as f:
    users = [userid.strip() for userid in f.readlines()]

## And also users from train triplets
users = set(users +  [user for user, _, _ in get_train_triplets()])

users_to_index = dict([(userid, idx) for (idx, userid) in enumerate(users)])


print("Building songs list...")

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


def load_taste_dataset_as_csc_matrix():
    try:
        return load_npz(csc_filepath)
    except:
        return generate_csc_matrix()


def generate_csc_matrix():
    global songs_to_index

    print("Processing listening counts...")

    users_to_songs = {}

    for user, song, count in get_train_triplets():
        count = int(count)

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

    # # Map songids to indexes
    # with open(songs_to_index_filepath, 'w') as outfile:
    #     songs_to_index = { song: i for i, song in enumerate(song_ids) }
    #     json.dump(songs_to_index, outfile, separators=(',', ':'))

    # # Map user ids to indexes
    # with open(users_to_index_filepath, 'w') as outfile:
    #     users_to_index = { user: i for i, user in enumerate(users_to_songs.keys()) }
    #     json.dump(users_to_index, outfile, separators=(',', ':'))


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

    ## Generate co-ocurrence matrix
    data = csc_matrix((data, (data_user_indexes, data_song_indexes)))

    # Persist data
    save_npz(csc_filepath, data)

    return data 


# try:
#     with open(users_to_index_filepath) as json_file:
#         users_to_index = json.load(json_file)
# except:
#     generate_csc_matrix()
#     with open(users_to_index_filepath) as json_file:
#         users_to_index = json.load(json_file)

# try:
#     with open(songs_to_index_filepath) as json_file:
#         songs_to_index = json.load(json_file)
# except:
#     generate_csc_matrix()
#     with open(songs_to_index_filepath) as json_file:
#         songs_to_index = json.load(json_file)







# Load data
X = load_taste_dataset_as_csc_matrix()
print("Loaded data")


# TODO: Normalize user listenings count: song count / total user counts



# Run matrix factorization
n_components = 200
start = timer()
print(f"Training with {n_components} components...")
model = TruncatedSVD(n_components, random_state=42)
W = model.fit_transform(X)
S = model.components_
end = timer()
elapsed = end - start
print(f"Traing done in {elapsed} seconds")

def predict(userid, songid):
    user_idx = users_to_index[userid]
    song_idx = int(songs_to_index[songid])

    return np.dot(W[user_idx], S[:, song_idx])

def predict_all(userid):
    user_idx = users_to_index[userid]

    return np.dot(W[user_idx], S)

    


# Predict example
print("\n==== Predict example ====")
print(
    predict("b80344d063b5ccb3212f76538f3d9e43d87dca9e", "SOIZAZL12A6701C53B")
)



print("\n\n====== EVALUATION ==========")
# Load evaluation users list
eval_users = []
with open(kaggle_users_filepath, "r") as f:
    eval_users = [line.strip() for line in f.readlines()]

print("\n==== Total eval users ====")
print(len(eval_users))

# Load evaluation songs list
eval_songs = []
with open(kaggle_songs_filepath, "r") as f:
    eval_songs = [id_and_index.strip().split(" ")[0] for id_and_index in f.readlines()]


# Load evaluation listening histories
eval_listen_count = {}
with open(eval_triplets_filepath, "r") as f:
    line = f.readline()
    while line:
        user, song, _ = line.strip().split("\t")
        songidx = songs_to_index[song]
        if user in eval_listen_count:
            eval_listen_count[user].add(songidx)
        else:
            eval_listen_count[user] = set([songidx])

        line = f.readline()


# Compute recommendations for evaluation users
recommendations = {}

for i, userid in enumerate(eval_users[:1000]):

    predictions = predict_all(userid)

    # To get a rank, we must revers the order
    # We also need to limit the rank to 500
    ranked = np.argsort(predictions)[::-1][:500]

    # user_song_scores = sorted(
    #     songs_to_index.keys(), 
    #     key=lambda songid: predictions[int(songs_to_index[songid])],
    #     reverse=True
    # )


    # recommendations[userid] = [songs_index_to_ids[idx] for idx in ranked]
    recommendations[userid] = ranked
    print(f"Generated recommendations for {i} users")


score = msd_mAP(
    recommendations,
    eval_listen_count
)

print("mAP: ", score)





