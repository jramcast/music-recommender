"""
Basic Collaborative Filtering Tutorial (K-means)

This tutorial is based on
https://heartbeat.fritz.ai/recommender-systems-with-python-part-ii-collaborative-filtering-k-nearest-neighbors-algorithm-c8dcd5fd89b2
"""

import os
import pandas as pd
import pathlib
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors


# Load data
movies_filename = "movie.csv"
ratings_filename = "rating.csv"
data_path = os.path.join(
    pathlib.Path(__file__).parent.absolute(),
    "../../../data/examples"
)

df_movies = pd.read_csv(
    os.path.join(data_path, movies_filename),
    usecols=["movieId", "title"],
    dtype={"movieId": "int32", "title": "str"}
)
df_ratings = pd.read_csv(
    os.path.join(data_path, ratings_filename),
    usecols=["userId", "movieId", "rating"],
    dtype={"userId": "int32", "movieId": "int32", "rating": "float32"}
)

# Only take first 10000 to make this example faster
df_ratings = df_ratings[:10000]

print("========= MOVIES DF =========")
print("MOVIES DF HEAD\n", df_movies.head(), end="\n\n")
print("MOVIES DF SHAPE", df_movies.shape, end="\n\n")

print("========= RATINGS DF =========")
print("RATINGS DF HEAD\n", df_ratings.head(), end="\n\n")
print("RATINGS DF SHAPE", df_ratings.shape, end="\n\n")


# Pivot ratings into movie features to get a rating matrix
# Each movie is a row and each user is a colum, values are ratings
# 0 indicates no rating
df_movie_features = df_ratings.pivot(
    index="movieId",
    columns="userId",
    values="rating"
).fillna(0)


print("========= MOVIE FEATURES DF =========")
print("MOVIE FEATURES DF HEAD\n", df_movie_features.head(), end="\n\n")
print("MOVIE FEATURES DF SHAPE", df_movie_features.shape, end="\n\n")

# Because many values are zero (the matrix is extremely sparse),
# we convert the matrix into a Compressed Sparse Matrix for better efficiency:
# https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.sparse.csr_matrix.html
mat_movie_features = csr_matrix(df_movie_features.values)


# To have and idea about users preferences:
# we need users that have rated more that 5 movies

popularity_thres = 5
df_movies_cnt = pd.DataFrame(
    df_ratings.groupby("movieId").size(),
    columns=["count"]
)
popular_movies = list(
    set(df_movies_cnt.query("count >= @popularity_thres").index
        ))
df_ratings_drop_movies = df_ratings[df_ratings.movieId.isin(popular_movies)]
print("shape of original ratings data: ", df_ratings.shape)
print(
    "shape of ratings data after dropping unpopular movies: ",
    df_ratings_drop_movies.shape
)

# The same goes for movies
ratings_thres = 5
df_users_cnt = pd.DataFrame(
    df_ratings_drop_movies.groupby("userId").size(),
    columns=["count"]
)
active_users = list(set(df_users_cnt.query("count >= @ratings_thres").index))
df_ratings_drop_users = df_ratings_drop_movies[
    df_ratings_drop_movies.userId.isin(active_users)
]
print("shape of original ratings data: ", df_ratings.shape)
print(
    "shape of ratings data after dropping unpopular/inactive movies/users: ",
    df_ratings_drop_users.shape
)


# Fit the Knn classifier
model_knn = NearestNeighbors(
    metric='cosine',
    algorithm='brute',
    n_neighbors=20,
    n_jobs=-1
)
model_knn.fit(mat_movie_features)
