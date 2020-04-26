"""
Recommender system for Million Song dataset (MSD),
 inspired in these 2 sources:

- Efficient top-n recommendation for very large scale binary rated datasets:
    https://dl.acm.org/doi/pdf/10.1145/2507157.2507189
- Million Song Dataset Challenge:
    https://www.kaggle.com/c/msdchallenge

- Get the dataset from: http://millionsongdataset.com/challenge/#data1

In particular, this experiment ....
"""

import numpy as np
from sklearn.metrics import average_precision_score

# TODO: download MSD: http://millionsongdataset.com/pages/getting-dataset/


# TODO: check song to track mapping with "taste_profile_song_to_tracks.txt"
# It seems songs are not the same as tracks
# More info here: https://www.kaggle.com/c/msdchallenge/data

"""
DATA Review:

The concatenation of EvalDataYear1MSDWebsite/*_visible seems to be 
the same as kaggle_challenge_files/kaggle_visible_evaluation_triplets.txt (check this)
Could this be our validation set?

My guess:
    - Public leaderboard uses: year1_valid_triplets_hidden.txt
    - Private leaderboard uses: year1_test_triplets_hidden.txt
    - EvalDataYear1MSDWebsite/*_visible seems to be 
the same as kaggle_challenge_files/kaggle_visible_evaluation_triplets.txt (for local testing)


EVALUATIN Metric (mAP):

https://www.kaggle.com/c/msdchallenge/discussion/1860



MORE INFO ON THE CHALLENGE AND EVALUATION METRIC
The Million Song Dataset Challenge, McFee, B., Bertin-Mahieux. T., Ellis, D.P.W., and Lanckriet, G.R.G.
4th International Workshop on Advances in Music Information Research (AdMIRe)
https://bmcfee.github.io/papers/msdchallenge.pdf
"""


y_true = np.array([1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0])
y_scores = np.array([0, 0.95, 0.1, 0.4, 0.4, 0.6, 0.8, 0.32, 0.33, 0.34, 0.35])
ap = average_precision_score(y_true, y_scores)
print(ap)


from sklearn.metrics import precision_recall_curve
import matplotlib.pyplot as plt


n_classes = 2
precision = {}
recall = {}
average_precision = {}


precision, recall, thresholds = precision_recall_curve(y_true, y_scores)
average_precision = average_precision_score(y_true, y_scores)

print("R", recall)
print("P", precision)
print("T", thresholds)
print("AP", average_precision)

plt.figure()
plt.step(recall, precision, where='post')

plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim([0.0, 1.05])
plt.xlim([0.0, 1.0])
plt.title('Average precision score={0:0.2f}'.format(average_precision))
plt.savefig("ap.png")


# Manual implementation: https://bmcfee.github.io/papers/msdchallenge.pdf equation 2

from sklearn.metrics import confusion_matrix

print("========== MANUAL ===============")

def precision_at_k(y_true, y_pred, k):
    tn, fp, fn, tp = confusion_matrix(y_true[:k], y_pred[:k]).ravel()
    return tp / k


predicted = np.array([1, 0, 1, 0, 1, 1, 0, 1, 0, 1])
real = np.array([0, 0, 1, 0, 1, 1, 0, 1, 0, 1])
K = 6


print(f"precision at {K}:", precision_at_k(real, predicted, K))


def ap(real, predicted, k):
    tn, fp, fn, tp = confusion_matrix(real, predicted).ravel()
    positives = tp + fp
    nu = min(k, positives)

    real_list = real.tolist()
    total = 0
    for i in range(k):
        if real_list[i] == 1:
            total += precision_at_k(real, predicted, i + 1)

    return total / nu


print("AP manual:", ap(real, predicted, K))
print("AP sklearn:", average_precision_score(real[:K], predicted[:K]))
