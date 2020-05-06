"""
Recommender system for Million Song dataset (MSD),
 inspired in these 2 sources:

- Efficient top-n recommendation for very large scale binary rated datasets:
    https://dl.acm.org/doi/pdf/10.1145/2507157.2507189
- Million Song Dataset Challenge:
    https://www.kaggle.com/c/msdchallenge

- Get the dataset from: http://millionsongdataset.com/challenge/#data1

In particular, this experiment ....


DATA Review:

The concatenation of EvalDataYear1MSDWebsite/*_visible seems to be 
the same as kaggle_challenge_files/kaggle_visible_evaluation_triplets.txt (check this)
Could this be our validation set?

My guess:
    - Public leaderboard uses: year1_valid_triplets_hidden.txt
    - Private leaderboard uses: year1_test_triplets_hidden.txt
    - EvalDataYear1MSDWebsite/*_visible seems to be 
the same as kaggle_challenge_files/kaggle_visible_evaluation_triplets.txt (for local testing)


EVALUATIN Metric (mAP):

https://www.kaggle.com/c/msdchallenge/discussion/1860



MORE INFO ON THE CHALLENGE AND EVALUATION METRIC
The Million Song Dataset Challenge, McFee, B., Bertin-Mahieux. T., Ellis, D.P.W., and Lanckriet, G.R.G.
4th International Workshop on Advances in Music Information Research (AdMIRe)
https://bmcfee.github.io/papers/msdchallenge.pdf
"""
import os
import pathlib

import sys
sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../../../.."
    )
)

from recommender.infrastructure.msd.loaders.songs import SongNotFound
from recommender.infrastructure.msd import loaders # noqa
from recommender.domain.recommend.regression import RegressionRecommender  # noqa


MSD_DATA_DIR = os.path.normpath(os.getenv("DATA_DIR") or os.path.join(
    pathlib.Path(__file__).parent.absolute(),
    "../../../../data/msdchallenge/MillionSongSubset/data"
))

MSD_CSV_FILEPATH = "data/msdchallenge/msd.csv"

KAGGLE_DATA_DIR = os.path.join(
    pathlib.Path(__file__).parent.absolute(),
    "../../../../data/msdchallenge/kaggle_challenge_files"
)

TASTE_PROFILE_DATA_DIR = os.path.join(
    pathlib.Path(__file__).parent.absolute(),
    "../../../../data/msdchallenge/TasteProfileDataset"
)

songs_filepath = os.path.join(
    KAGGLE_DATA_DIR, "kaggle_songs.txt"
)

print("Loading kaggle song indexes")
song_kaggle_indexes = loaders.kagglesongs.load(KAGGLE_DATA_DIR)
print(f"{len(song_kaggle_indexes.keys())} songs in kaggle competition")

print("Loading songs")
songs = {}
for songid, song_kaggleidx in song_kaggle_indexes.items():
    try:
        songs[songid] = loaders.songs.find(songid, MSD_DATA_DIR)
    except SongNotFound:
        print(f"Track for song {songid} not found in dataset")

print(f"Loaded {len(songs)}")

# songs = loaders.songs.load(MSD_CSV_FILEPATH)

# print("Loading users")
# users = loaders.users.load(KAGGLE_DATA_DIR)

# print("Loading users to songs training set")
# user_to_songs_train = loaders.taste.load_training_set(TASTE_PROFILE_DATA_DIR)

# print("Loading users to songs evaluation set")
# user_to_songs_eval = loaders.taste.load_evaluation_set(KAGGLE_DATA_DIR)


# recommender = RegressionRecommender(
#     user_to_songs_train,
#     user_to_songs_eval,
#     songs
# )

# recommender.train()
