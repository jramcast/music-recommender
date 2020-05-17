import numpy as np
import pandas as pd


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

model = NMF(n_components=4, init='random', random_state=0)
W = model.fit_transform(data)

print("Song latent factors matrix (Num users * Num factors)")
# print(W)

S = model.components_
print("User latent factors matrix (Num factors * Num songs)")
# print(S)

print("Reconstructed matrix: W * S")
reconstructed = pd.DataFrame(np.dot(W, S), columns=columns)
reconstructed.index = index
print(reconstructed)