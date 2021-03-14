import time

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
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
        return results['mean_test_score'][0], results['std_test_score'][1], results['params'][1]['criterion'], \
               results['params'][1]['n_estimators']


def my_model(param_def, clf=RandomForestClassifier()):
    # specify parameters and distributions to sample from
    param_dist = {'n_estimators': [(j) for j in range(1, 100)],
                  'criterion': ['gini', 'entropy']}

    # run randomized search

    # Cross validation
    cv = ShuffleSplit(n_splits=20, test_size=0.3, random_state=0)
    random_search = GridSearchCV(clf, param_grid=param_dist, cv=cv, iid=False)
    start = time.time()
    random_search.fit(param_def[1], y)
    print("RandomizedSearchCV took %.2f seconds for %d candidates"
          " parameter settings." % ((time.time() - start), 3))
    score, std, criterion, n_estimators = report(random_search.cv_results_)
    array.append([param_def[0], score, std, criterion, n_estimators])


if __name__ == '__main__':
    test = (True, 'work_with_time_based')
    # Save the results
    array = []
    # Upload and prepare  data
    df = pd.read_csv('csv_files/results.csv')
    X = df.loc[:, df.columns[1:14]].to_numpy()
    y = df.loc[:, df.columns[14]].to_numpy()

    # Set a dictionary that store X (training set) each time exclude different feature/s
    parameters = {'exclude_time': df.loc[:, df.columns[1:12]].to_numpy(),
                  'exclude_spatial_features': df.loc[:, df.columns[10:14]].to_numpy(),
                  'exclude_space_syntax': pd.concat([df.loc[:, df.columns[1:10]], df.loc[:, df.columns[12:14]]],
                                                    axis=1).to_numpy()}
    for i in range(1, 14):
        parameters[df.columns[i]] = pd.concat([df.loc[:, df.columns[1:i]], df.loc[:, df.columns[1 + i:14]]],
                                              axis=1).to_numpy()
    # Initial MLPClassifier
    if test[0]:
        for param in parameters.items():
            my_model(param)
    else:
        my_model(parameters[test[1]])
    # save the results
    df = pd.DataFrame(array,
                      columns=['name', 'mean_test_score', 'std_test_score', "criterion", "n_estimators"])
    if test[0]:
        df.to_csv('csv_files/analysis_features.csv')
    else:
        df.to_csv('csv_files/' + test[1] + 'analysis_features.csv')
