import pandas as pd
from sklearn import svm
from sklearn import tree
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import cross_validate
from sklearn.neural_network import MLPClassifier

if __name__ == '__main__':
    algorithm_dictionary = {'random forest': RandomForestClassifier(), 'ANN': MLPClassifier(max_iter=400),
                            'SVM': svm.SVC(), 'SGD': SGDClassifier(), 'ada Boost': AdaBoostClassifier(),
                            'Decision Tree': tree.DecisionTreeClassifier()}
    # Upload and prepare  data
    df = pd.read_csv('csv_files/results.csv')

    X = df.loc[:, df.columns[1:14]].to_numpy()
    y = df.loc[:, df.columns[14]].to_numpy()
    res_list = []
    # Initial MLPClassifier
    for clf in algorithm_dictionary.items():
        # # specify parameters and distributions to sample from
        # # Cross validation
        print(clf[0])

        cv = ShuffleSplit(n_splits=20, test_size=0.3, random_state=0)

        scoring = ['accuracy', 'f1', 'f1_micro', 'precision', 'recall']
        scores = cross_validate(clf[1], X, y, cv=cv, scoring=scoring, n_jobs=-1)
        mean = scores['test_accuracy'].mean()
        std = scores['test_accuracy'].std()
        print("Accuracy :%0.3f (+/- %0.4f)" % (mean, std))
        print("test_f1 : %0.3f (+/- %0.4f)" % (scores['test_f1'].mean(), scores['test_f1'].std()))
        print("test_f1_micr : %0.3f (+/- %0.4f)" % (scores['test_f1_micro'].mean(), scores['test_f1_micro'].std()))
        print("test_precision : %0.3f (+/- %0.4f)" % (
            scores['test_precision'].mean(), scores['test_precision'].std()))
        print("test_recall : %0.3f (+/- %0.4f)" % (scores['test_recall'].mean(), scores['test_recall'].std()))

        res_list.append(
            [clf[0], mean, std, scores['test_f1'].mean(), scores['test_f1'].std(), scores['test_precision'].mean(),
             scores['test_precision'].std(),
             scores['test_recall'].mean(), scores['test_recall'].std()])

df = pd.DataFrame(res_list,
                  columns=['name', 'accuracy', 'accuracy_std', 'f1', 'f1_std', 'precision', 'precision_std', 'recall',
                           'recall_std'])

df.to_csv('matrices')
