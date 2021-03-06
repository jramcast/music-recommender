"""
Recommender system for Million Song dataset (MSD),
 inspired in these 2 sources:

- Efficient top-n recommendation for very large scale binary rated datasets:
    https://dl.acm.org/doi/pdf/10.1145/2507157.2507189
- Million Song Dataset Challenge:
    https://www.kaggle.com/c/msdchallenge

In particular, this experiment uses the code in MSDChallengeGettingstarted.pdf
It is a baseline implementation based on song popularity.
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
from recommender.domain.scoring import msd_average_precision, msd_mAP

data_path = os.path.join(
    pathlib.Path(__file__).parent.absolute(),
    "../../../../data/msdchallenge/kaggle_challenge_files"
)

eval_triplets_filepath = os.path.join(
    data_path, "kaggle_visible_evaluation_triplets.txt"
)
users_filepath = os.path.join(
    data_path, "kaggle_users.txt"
)
songs_filepath = os.path.join(
    data_path, "kaggle_songs.txt"
)

# Load song popularity as song play count

song_to_count = {}

with open(eval_triplets_filepath, "r") as f:
    line = f.readline()
    while line:
        _, song, _ = line.strip().split("\t")
        if song in song_to_count:
            song_to_count[song] += 1
        else:
            song_to_count[song] = 1

        line = f.readline()

# Order songs by popularity
songs_ordered = sorted(
    song_to_count.keys(),
    key=lambda s: song_to_count[s],
    reverse=True
)

print("\n========= Top-5 popular songs ==========")
print(songs_ordered[:5])


# Load full users list
canonical_users = []
with open(users_filepath, "r") as f:
    canonical_users = [line.strip() for line in f.readlines()]

print("\n==== Users head ====")
print(canonical_users[:5])


# Load full songs list to map song ID to index
song_to_index = {}
with open(songs_filepath, "r") as f:
    song_to_index = dict(
        [id_and_index.strip().split(" ") for id_and_index in f.readlines()]
    )

# Load songs each user's listening history
user_to_songs = {}
user_to_song_ids = {}
with open(eval_triplets_filepath, "r") as f:
    line = f.readline()
    while line:
        user, song, _ = line.strip().split("\t")
        song_index = song_to_index[song]
        if user in user_to_songs:
            user_to_songs[user].add(song)
            user_to_song_ids[user].add(song_index)
        else:
            user_to_songs[user] = set([song])
            user_to_song_ids[user] = set([song_index])

        line = f.readline()

print("\n===== Example of user library =====")
print(user_to_songs["d7083f5e1d50c264277d624340edaaf3dc16095b"])


# Recommend popular songs to each user,
# leaving out those already in the users's listening history

print("\n\n\n Computing recommendations...", end='')

recommendations = {}

for user in canonical_users:
    songs_to_recommend = []
    for song in songs_ordered:
        if len(songs_to_recommend) >= 500:
            break
        if song not in user_to_songs[user]:
            songs_to_recommend.append(song)

    song_indices = [song_to_index[song] for song in songs_to_recommend]
    recommendations[user] = song_indices



print("\n\n====== EVALUATION ==========")


# print(canonical_users[:2])
# print([list(recommendations[key])[:2] for key in list(recommendations.keys())[:2]])
# print([list(user_to_song_ids[key])[:2] for key in list(user_to_song_ids.keys())[:2]])

# exit()

score = msd_mAP(
    canonical_users,
    recommendations,
    user_to_song_ids
)

print("mAP", score)


print("\n\n==== RECOMMENDATION EXAMPLE ==========")

test_user = "b584c8326c8f79052d8d2adae67afb9da248b3df"
recommended_for_user = recommendations[test_user]
print(f"\nUser: {test_user}. "
      + f"Recommended songs: {recommended_for_user[:5]}...")
