#!/usr/bin/env python


"""
Recommender basic test
based on cosine similarity between vectors of "preferences" and recommended songs
https://www.mendeley.com/viewer/?fileId=20d7cbe3-573e-fc75-63c3-8e1f174869a8&documentId=28288f63-525b-3f5d-a309-a7d1b9281c25
"""

# example of a bimodal constructed from two gaussian processes
from numpy import hstack
from numpy.random import normal
from matplotlib import pyplot
# generate a sample
X1 = normal(loc=20, scale=5, size=3000)
X2 = normal(loc=40, scale=5, size=7000)
X = hstack((X1, X2))
# plot the histogram
pyplot.hist(X, bins=50, density=True)
pyplot.show()



from sklearn.mixture import GaussianMixture

LATENT_VARIABLES=2

# reshape into a table with one column
X = X.reshape((len(X), 1))

# TRAIN
model = GaussianMixture(n_components=LATENT_VARIABLES, init_params='random')
model.fit(X)
# predict latent values
yhat = model.predict(X)
# check latent value for first few points
print(yhat[:100])
# check latent value for last few points
print(yhat[-100:])