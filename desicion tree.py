import pickle
import time

import numpy as np
import pandas as pd
from sklearn import tree
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import ShuffleSplit


# Utility function to report best scores
def report(results, n_top=3):
    for i in range(1, n_top + 1):
        candidates = np.flatnonzero(results['rank_test_score'] == i)
        for candidate in candidates:
            print("Model with rank: {0}".format(i))
            print("Mean validation score: {0:.3f} (std: {1:.3f} , min:{2:.3f})".format(
                results['mean_test_score'][candidate],
                results['std_test_score'][candidate],
                results['mean_test_score'][candidate] - results['std_test_score'][candidate] * 2))
            print("Parameters: {0}".format(results['params'][candidate]))
            print("")


if __name__ == '__main__':
    # Upload and prepare  data
    df = pd.read_csv('csv_files/results.csv')

    df = pd.read_csv('csv_files/results.csv')
    X = df.loc[:, df.columns[1:14]].to_numpy()
    y = df.loc[:, df.columns[14]].to_numpy()

    # Initial MLPClassifier
    clf = tree.DecisionTreeClassifier()

    # specify parameters and distributions to sample from
    param_dist = {'criterion': ['gini', 'entropy'],
                  'max_features': [1, 2, 3, 4, 5, 6, 7, 8, 10, 'sqrt', 'log2', 'None']}

    # run randomized search

    # Cross validation
    cv = ShuffleSplit(n_splits=20, test_size=0.3, random_state=0)
    random_search = GridSearchCV(clf, param_grid=param_dist, cv=cv, iid=False, n_jobs=-1)
    start = time.time()
    random_search.fit(X, y)
    print("RandomizedSearchCV took %.2f seconds for %d candidates"
          " parameter settings." % ((time.time() - start), 3))
    report(random_search.cv_results_)
    pickle.dumps(clf)
