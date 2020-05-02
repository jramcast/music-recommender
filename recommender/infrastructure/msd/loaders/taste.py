"""
Code to read 'Taste Profile subset' data
http://millionsongdataset.com/tasteprofile/
"""
import os


def load_training_set(data_dir):
    """
    Load triplets of user,song,playcount list from
    The Echo Nest Taste Profile Subset
    """
    filepath = os.path.join(
        data_dir, "train_triplets.txt"
    )

    return _load(filepath)


def load_evaluation_set(data_dir):
    """
    Load triplets of user,song,playcount list from
    The Echo Nest Taste Profile Subset
    """
    filepath = os.path.join(
        data_dir, "kaggle_visible_evaluation_triplets.txt"
    )

    return _load(filepath)


def _load(filepath):
    user_to_songs = {}

    with open(filepath, "r") as f:
        line = f.readline()
        while line:
            userid, songid, _ = line.strip().split("\t")
            if userid in user_to_songs:
                user_to_songs[userid].add(songid)
            else:
                user_to_songs[userid] = set([songid])

            line = f.readline()

    return user_to_songs
