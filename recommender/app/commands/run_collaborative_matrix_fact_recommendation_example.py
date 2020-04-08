"""
Basic Collaborative Filtering Tutorial (Matrix factorization)

This tutorial is based on
https://heartbeat.fritz.ai/recommender-systems-with-python-part-iii-collaborative-filtering-singular-value-decomposition-5b5dcb3f242b
"""

import os
import pathlib
import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds


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
df_ratings = df_ratings[:100000]


print("========= MOVIES DF =========")
print("MOVIES DF HEAD\n", df_movies.head(), end="\n\n")
print("MOVIES DF SHAPE", df_movies.shape, end="\n\n")

print("========= RATINGS DF =========")
print("RATINGS DF HEAD\n", df_ratings.head(), end="\n\n")
print("RATINGS DF SHAPE", df_ratings.shape, end="\n\n")


# RATING MATRIX
# Pivot ratings into movie features to get a rating matrix
# Each movie is a row and each user is a colum, values are ratings
# 0 indicates no rating
df_movie_features = df_ratings.pivot(
    index='userId',
    columns='movieId',
    values='rating'
).fillna(0)

print("========= RATINGS MATRIX (Movies x Users) =========")
print("RATINGS MATRIX: HEAD\n", df_movie_features.head(), end="\n\n")
print("RATINGS MATRIX: SHAPE", df_movie_features.shape, end="\n\n")

# Normalize each user's ratings (demeaning) to remove user bias
# If a user tends to rate low, 3 actually means a top rating in his own scale
# and that’s the information we want to extract
R = df_movie_features.to_numpy()
user_ratings_mean = np.mean(R, axis=1)
R_demeaned = R - user_ratings_mean.reshape(-1, 1)

print("Factorizing matrix...")
# Perform matrix factorization with Singular Value Decomposition (SVD)
U, sigma, Vt = svds(R_demeaned, k=50)
# The returned value in sigma is just the values instead of a diagonal matrix.
# Since I'm going to leverage matrix multiplication to get predictions
# I'll convert it to the diagonal matrix form.
sigma = np.diag(sigma)
all_user_predicted_ratings = np.dot(
    np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)

print("========= USER PREDICTED RATINGS =========")
print("USER PREDICTED RATINGS:\n",
      all_user_predicted_ratings, end="\n\n")
print("USER PREDICTED RATINGS: SHAPE",
      all_user_predicted_ratings.shape, end="\n\n")


def recommend_movies(
        preds_df,
        userID,
        movies_df,
        original_ratings_df,
        num_recommendations=5):
    """
    Get and sort the user's predictions
    """
    # UserID starts at 1, not 0
    user_row_number = userID - 1
    sorted_user_predictions = preds_df.iloc[user_row_number].sort_values(
        ascending=False)  # UserID starts at 1
    # Get the user's data and merge in the movie information.
    user_data = original_ratings_df[original_ratings_df.userId == (userID)]
    user_full = (user_data.merge(movies_df, how='left', left_on='movieId', right_on='movieId').
                 sort_values(['rating'], ascending=False)
                 )

    recommendations = (movies_df[~movies_df['movieId'].isin(user_full['movieId'])]).merge(pd.DataFrame(sorted_user_predictions).reset_index(), how='left', left_on='movieId',
                                                                                          right_on='movieId').rename(columns={user_row_number: 'Predictions'}).sort_values('Predictions', ascending=False).iloc[:num_recommendations, :-1]

    return user_full, recommendations


if __name__ == "__main__":

    preds_df = pd.DataFrame(all_user_predicted_ratings,
                            columns=df_movie_features.columns)

    already_rated, predictions = recommend_movies(
        preds_df, 330, df_movies, df_ratings, 10)

    print("========= PREDICTIONS =========")
    print("USER RATED MOVIES:\n")
    print(already_rated.head())

    print("PREDICTED MOVIES FOR USER\n")
    print(predictions)
