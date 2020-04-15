"""
TODO: Create a recommender system for Million Song dataset (MSD) inspired in this 2 sources:

- Efficient top-n recommendation for very large scale binary rated datasets: https://dl.acm.org/doi/pdf/10.1145/2507157.2507189
- Million Song Dataset Challenge: https://www.kaggle.com/c/msdchallenge
"""

import os
import pathlib

data_path = os.path.join(
    pathlib.Path(__file__).parent.absolute(),
    "../../../data/msdchallenge"
)

eval_triplets_filepath = os.path.join(
    data_path, "kaggle_visible_evaluation_triplets.txt"
)

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

print(song_to_count)
