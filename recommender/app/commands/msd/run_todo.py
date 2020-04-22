"""
Recommender system for Million Song dataset (MSD),
 inspired in these 2 sources:

- Efficient top-n recommendation for very large scale binary rated datasets:
    https://dl.acm.org/doi/pdf/10.1145/2507157.2507189
- Million Song Dataset Challenge:
    https://www.kaggle.com/c/msdchallenge

- Get the dataset from: http://millionsongdataset.com/challenge/#data1

In particular, this experiment ....
"""

# TODO: download MSD: http://millionsongdataset.com/pages/getting-dataset/


# TODO: check song to track mapping with "taste_profile_song_to_tracks.txt"
# It seems songs are not the same as tracks
# More info here: https://www.kaggle.com/c/msdchallenge/data

"""
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
"""
