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

import math
import pathlib
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
csc_filepath = os.path.join(
    data_path, "csc_matrix.npz"
)
songs_to_index_filepath = os.path.join(
    data_path, "songs_to_index.json"
)
users_to_index_filepath = os.path.join(
    data_path, "users_to_index.json"
)

kaggle_triplets_filepath = os.path.join(
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

# ## And also users from train triplets
# users = set(users +  [user for user, _, _ in get_train_triplets()])

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
    return generate_csc_matrix()
    # try:
    #     return load_npz(csc_filepath)
    # except:
    #     return generate_csc_matrix()

validation_triplets = {}
train_triplets = {}
eval_users = set()
train_users = set()

def generate_csc_matrix():
    global songs_to_index, validation_triplets, train_triplets

    print("Processing listening counts...")

    # Load listening histories from kaggle
    # Half to train, other half to validation
    triplets_for_matrix = {}
    next_for_train = True
    i = 0
    with open(kaggle_triplets_filepath, "r") as f:
        line = f.readline()
        while line:
            user, song, count = line.strip().split("\t")
            count = 1 if int(count) > 0 else 0
            songidx = songs_to_index[song]

            if i % 1000 == 0:
                if user in validation_triplets:
                    validation_triplets[user].add(songidx)
                else:
                    validation_triplets[user] = set([songidx])

                next_for_train = not next_for_train
                eval_users.add(user)

            else:
                if user in train_triplets:
                    # No user-song duplicates
                    # if song in users_to_songs[user]:
                    #     users_to_songs[user][song] += count
                    # else:
                    #     users_to_songs[user][song] = count
                    train_triplets[user].add(songidx)
                    triplets_for_matrix[user][song] = count
                else:
                    train_triplets[user] = set([songidx])
                    triplets_for_matrix[user] = { song: count }

                train_users.add(user)

            i += 1

            line = f.readline()

    # # Normalization
    # for user in triplets_for_matrix.keys():
    #     songs = triplets_for_matrix[user]
    #     sum_counts = 0
    #     for songid in songs.keys():
    #         sum_counts += songs[songid]
    #     count_avg = sum_counts / len(songs.keys())

    #     # Handle outliers
    #     deviation = 0
    #     for songid in songs.keys():
    #         deviation += (songs[songid] - count_avg) ** 2

    #     deviation = math.sqrt(deviation / count_avg)

    #     for songid in songs.keys():
    #         if songs[songid] > count_avg + deviation:
    #             songs[songid] = count_avg + deviation

    #     # After handling outliers, recalculate count avg, get min and max
    #     sum_counts = 0
    #     count_values = []
    #     for songid in songs.keys():
    #         sum_counts += songs[songid]
    #         count_values.append(songs[songid])
    #     min_count = min(count_values)
    #     max_count = max(count_values)
    #     count_avg = sum_counts / len(songs.keys())

    #     # Normalize
    #     for songid in songs.keys():
    #         songs[songid] = songs[songid] / sum_counts


    # for user, song, count in get_train_triplets():
    #     count = int(count)

    #     if song not in songs_to_index:
    #         print("song " + song + " not in song_to_idex")

    #     if user in triplets_for_matrix:
    #         # No user-song duplicates
    #         # if song in users_to_songs[user]:
    #         #     users_to_songs[user][song] += count
    #         # else:
    #         #     users_to_songs[user][song] = count
    #         triplets_for_matrix[user][song] = count
    #     else:
    #         triplets_for_matrix[user] = { song: count }

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

        for songid in triplets_for_matrix.get(user, {}).keys():

            play_count = triplets_for_matrix[user][songid]
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


# Load data
X = load_taste_dataset_as_csc_matrix()
print("Loaded data")


# Run matrix factorization
n_components = 2
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
    predict("d7083f5e1d50c264277d624340edaaf3dc16095b", "SOEFCDJ12AB0185FA0")
)



print("\n\n====== EVALUATION ==========")


def evaluate(users, actual_triplets, drop={}):

    # Compute recommendations for evaluation users
    recommendations = {}

    for i, userid in enumerate(users):
        predictions = predict_all(userid)

        # Do not recommend already known songs
        indexes_to_drop = list(drop.get(userid, []))
        np.put(predictions, indexes_to_drop, 0)

        # To get a rank, we must revers the order
        # We also need to limit the rank to 500
        ranked = np.argsort(predictions)[::-1][:500]

        # recommendations[userid] = [songs_index_to_ids[idx] for idx in ranked]
        recommendations[userid] = ranked
        if i > 0 and i % 100 == 0:
            print(f" computed {i} of {len(users)} users")

    return msd_mAP(
        recommendations,
        actual_triplets
    )

print("mAP for training set: ", evaluate(
    list(train_users)[:200], train_triplets
))
print("mAP for validation set: ", evaluate(
    list(eval_users), validation_triplets, drop=train_triplets
))





