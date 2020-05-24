import numpy as np
import pandas as pd

#  We use the the song latent factor matrix extracted from matrix factorization
#  and then predict a classifier that, given a song features, predicts these latent factors.
#  
#  Inspired in:
#  https://medium.com/logicai/non-negative-matrix-factorization-for-recommendation-systems-985ca8d5c16c
#
# Run with docker GPU: docker run --gpus all -v $(pwd):/app -it --rm tensorflow/tensorflow:latest-gpu bash


# Create a example user-to-song rating matrix
index = ["u1", "u2", "u3"]
columns = [f"song{i}" for i in range(1, 6)]
data = pd.DataFrame(
    [
        [0, 7, 4, 4, 3],
        [4, 0, 0, 2, 9],
        [10, 5, 2, 8, 0],
    ],
    columns=columns
)
data.index = index

print(data)


import numpy as np
from sklearn.decomposition import NMF

model = NMF(n_components=4, init="random", random_state=0)
W = model.fit_transform(data)

print("Song latent factors matrix (Num users * Num factors)")
# print(W)

S = model.components_
print("User latent factors matrix (Num factors * Num songs)")
# print(S)


# Create an example matrix of song features
songindex = ["s1", "s2", "s3", "s4", "s5"]
featcolums = [f"feat{i}" for i in range(1, 6)]
songs = pd.DataFrame(
    [
        [0, 1, 0.4, 0.2, 0.3],
        [0.1, 0.3, 0.7, 0.2, 0.67],
        [0.03, 0.3, 0.1, 0.8, 0.2],
        [0.2, 0.3, 0.1, 0.8, 0.6],
        [0.6, 0.3, 0.6, 0.3, 0.3],
    ],
    columns=featcolums
)
songs.index = songindex


print("Song low-level audio features")
print(songs)



# Train a NN that predicts latent factors, given song features
print("Train ")
import tensorflow as tf
mnist = tf.keras.datasets.mnist

y = S.transpose()
x_train = songs[:3]
y_train = y[:3]
x_test = songs[3:]
y_test = y[3:]

print(y_train.shape)

model = tf.keras.models.Sequential([
  tf.keras.layers.Input(shape=(5)),
  tf.keras.layers.Dense(12800, activation="relu"),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(1600, activation="relu"),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(80, activation="relu"),
  tf.keras.layers.Dense(80, activation="relu"),
  tf.keras.layers.Dense(80, activation="relu"),
  tf.keras.layers.Dense(80, activation="relu"),
  tf.keras.layers.Dense(80, activation="relu"),
  tf.keras.layers.Dense(80, activation="relu"),
  tf.keras.layers.Dense(80, activation="relu"),
  tf.keras.layers.Dense(4)
])

model.compile(optimizer="adam",
              loss="mse",
              metrics=['mae', 'mse'])

model.fit(x_train, y_train, epochs=50)


mse, mae, mse = model.evaluate(x_test, y_test, verbose=2)



print('\nTest mean absolute error:', mae)

