import numpy as np
import pandas as pd
from pgmpy.models import BayesianModel
from pgmpy.estimators import HillClimbSearch, BicScore, BayesianEstimator

# Learn a bayesian network structure from data
#
# https://github.com/pgmpy/pgmpy_notebook/blob/master/notebooks/9.%20Learning%20Bayesian%20Networks%20from%20Data.ipynb

# Create
songindex = [f"song{i}" for i in range(1, 100)]
featcolums = ["electronic", "house", "lowfi", "ambient", "relaxing", "sad", "happy", "party", "techno"]
n = len(songindex)
m = len(featcolums)
onehotmatrix = np.random.choice([0, 1], size=[n, m])
np.random.shuffle(onehotmatrix)
data = pd.DataFrame(onehotmatrix, columns=featcolums)
data.index = songindex
print(data.head())


bic = BicScore(data)
hc = HillClimbSearch(data, scoring_method=BicScore(data))
best_model = hc.estimate()
print("Structure: ", best_model.edges())


model = BayesianModel(best_model.edges())  

model.fit(data, estimator=BayesianEstimator, prior_type="BDeu") 
for cpd in model.get_cpds():
    print(cpd)
