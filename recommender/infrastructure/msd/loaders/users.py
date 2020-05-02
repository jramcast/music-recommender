import os


def load(data_dir):
    """
    Load users list from Kaggle data
    """
    users_filepath = os.path.join(
        data_dir, "kaggle_users.txt"
    )

    with open(users_filepath, "r") as f:
        return [line.strip() for line in f.readlines()]
