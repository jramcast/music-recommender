import os


def load(data_dir):
    """
    Loads songs included in the Kaggle challenge
    The data maps song ids to an incremental song index
    """
    songs_filepath = os.path.join(data_dir, "kaggle_songs.txt")

    song_ids_to_index = {}

    with open(songs_filepath, "r") as f:
        song_ids_to_index = dict(
            [id_and_index.strip().split(" ") for id_and_index in f.readlines()]
        )

    return song_ids_to_index
