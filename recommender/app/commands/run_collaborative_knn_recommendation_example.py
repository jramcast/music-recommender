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
from fuzzywuzzy import fuzz


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


# Most of the movies in the dataset do not have any rating,
# so we will only take in account those users
# that have rated more than 5 movies
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

# Similarly, we only take into account those movies that have been rated
# more than 5 times
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


# RATING MATRIX
# Pivot ratings into movie features to get a rating matrix
# Each movie is a row and each user is a colum, values are ratings
# 0 indicates no rating
movie_user_mat = df_ratings_drop_movies.pivot(
    index="movieId",
    columns="userId",
    values="rating"
).fillna(0)

print("========= MOVIE FEATURES DF =========")
print("MOVIE FEATURES DF HEAD\n", movie_user_mat.head(), end="\n\n")
print("MOVIE FEATURES DF SHAPE", movie_user_mat.shape, end="\n\n")

# Because many values are zero (the matrix is extremely sparse),
# we convert the matrix into a Compressed Sparse Matrix for better efficiency:
# https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.sparse.csr_matrix.html
movie_user_mat_sparse = csr_matrix(movie_user_mat.values)

# We also need a map of movie titles to ids for pretty printing
movies_list = list(
    df_movies.set_index("movieId").loc[movie_user_mat.index].title
)
movie_to_idx = {
    movie: i for i, movie in enumerate(movies_list)
}


# Fit the Knn classifier
model_knn = NearestNeighbors(
    metric="cosine",
    algorithm="brute",
    n_neighbors=20,
    n_jobs=-1
)
print("Training........")
model_knn.fit(movie_user_mat_sparse)


def make_recommendation(model_knn, data, mapper, fav_movie, n_recommendations):
    """
    return top n similar movie recommendations based on user"s input movie
    Parameters
    ----------
    model_knn: sklearn model, knn model
    data: movie-user matrix
    mapper: dict, map movie title name to index of the movie in data
    fav_movie: str, name of user input movie
    n_recommendations: int, top n recommendations
    Return
    ------
    list of top n similar movie recommendations
    """
    # fit
    model_knn.fit(data)
    # get input movie index
    print("You have input movie:", fav_movie)
    idx = fuzzy_matching(mapper, fav_movie, verbose=True)

    print("Recommendation system start to make inference")
    print("......\n")
    distances, indices = model_knn.kneighbors(
        data[idx], n_neighbors=n_recommendations+1)

    raw_recommends = sorted(list(zip(indices.squeeze().tolist(
    ), distances.squeeze().tolist())), key=lambda x: x[1])[:0:-1]
    # get reverse mapper
    reverse_mapper = {v: k for k, v in mapper.items()}
    # print recommendations
    print("Recommendations for {}:".format(fav_movie))
    for i, (idx, dist) in enumerate(raw_recommends):
        print("{0}: {1}, with distance of {2}".format(
            i+1, reverse_mapper[idx], dist))


def fuzzy_matching(mapper, fav_movie, verbose=True):
    """
    return the closest text match via fuzzy ratio.

    Parameters
    ----------
    mapper: dict, map movie title name to index of the movie in data
    fav_movie: str, name of user input movie

    verbose: bool, print log if True
    Return
    ------
    index of the closest match
    """
    match_tuple = []
    # get match
    for title, idx in mapper.items():
        ratio = fuzz.ratio(title.lower(), fav_movie.lower())
        if ratio >= 60:
            match_tuple.append((title, idx, ratio))
    # sort
    match_tuple = sorted(match_tuple, key=lambda x: x[2])[::-1]
    if not match_tuple:
        print("Oops! No match is found")
        return
    if verbose:
        print("Found possible matches in our database: {0}\n".format(
            [x[0] for x in match_tuple]))
    return match_tuple[0][1]


if __name__ == "__main__":
    """
    Test the recommendation model:
    K-nn has issues:
    * popularity bias
    * item cold-start: new movies won't have ratings,
        hence won't be recommended
    * scalability: most of the values in the ratings(movie-user)
         sparse matrix will be 0, which is a waste of space.
    """
    my_favorite = "Toy Story"

    make_recommendation(
        model_knn=model_knn,
        data=movie_user_mat_sparse,
        fav_movie=my_favorite,
        mapper=movie_to_idx,
        n_recommendations=10
    )
