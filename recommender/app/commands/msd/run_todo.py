import pandas as pd

songs = pd.read_csv("data/songs_with_features.csv")

user_songs = pd.read_csv(
    "data/msdchallenge/TasteProfileDataset/train_triplets.txt", 
    sep="\t",
    names=["userid", "songid", "playcount"
])

print(user_songs.head())