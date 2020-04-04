"""
Basic Content Filtering Tutorial

This tutorial is based on
https://heartbeat.fritz.ai/recommender-systems-with-python-part-i-content-based-filtering-5df4940bd831
"""
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


DATASET_URL = (
    "https://raw.githubusercontent.com/nikitaa30/" +
    "Content-based-Recommender-System/master/sample-data.csv"
)

dataset = pd.read_csv(DATASET_URL)

print("========= DATASET =========")
print("DATASET HEAD", dataset.head(), end="\n\n")
print("DATASET SHAPE", dataset.shape, end="\n\n")

# Create TDIF vectorizer to calculate word weights
tf = TfidfVectorizer(
    analyzer='word',
    ngram_range=(1, 3),
    min_df=0,
    stop_words='english'
)
tfidf_matrix = tf.fit_transform(dataset['description'])

print("========= TDIF matrix =========")
tfidf_matrix_arr = tfidf_matrix.toarray()
print(tfidf_matrix_arr, end="\n\n")
print("TDIF SHAPE", tfidf_matrix_arr.shape, end="\n\n")


# Calculate cosine similarities between each element
# in the TDIF matrix. An element has a cosine similarity
# of 1, whereas completely different elements produce 0

# Linear kernel is equivalent to cosine similarity
# in cases where td-idf produces normalized vectors
# https://scikit-learn.org/stable/modules/metrics.html#cosine-similarity
similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

print("======= SIMILARITIES matrix ===========")
print(similarities, end="\n\n")
print("SIMILARITIES shape", similarities.shape, end="\n\n")

results = {}
for idx, row in dataset.iterrows():
    # Take indices of the top 100 most similar elements
    similar_indices = similarities[idx].argsort()[:-100:-1]

    # Generate list of similar items (on for each similar index)
    similar_items = []
    for i in similar_indices:
        similar_items.append((similarities[idx][i], dataset['id'][i]))

    # All similar items but itself (indexed by item ID)
    results[row['id']] = similar_items[1:]


def recommend_similar_to(item_id, num):
    print(f"Recommending {num} products similar to" +
          f" '{print_item(item_id)} (ID {item_id})'")
    print("-------")
    recs = results[item_id][:num]
    for rec in recs:
        print("Recommended: " +
              print_item(rec[1]) + " (score:" + str(rec[0]) + ")")


def print_item(id):
    item = dataset.loc[dataset['id'] == id]
    title = item['description'].tolist()[0].split(" - ")[0]
    return title


if __name__ == "__main__":
    print("*************** RECOMMENDATIONS ****************")
    item_id = int(os.environ.get("ITEM_ID", "1"))
    recommend_similar_to(item_id, num=5)
