import numpy as np
import pandas as pd

# concatenate uncontentious columns in dataframe into new one
df = pd.DataFrame(np.random.randn(6, 3), columns=['A', 'B', 'C'],dtype=str)
print(df)
print(df.loc[:, df.columns[0]])
# df = pd.concat([df.loc[:, df.columns[0]], df.loc[:, df.columns[2]]], axis=1).to_numpy()
# df = pd.concat(df.loc[:, df.columns[0]], df.loc[:, df.columns[2]])
# print(df)
# MultiIndex for index
# arrays = [
#     ['Sunday', 'Sunday', 'Monday', 'Monday', 'Tuesday', 'Tuesday', 'Wednesday', 'Wednesday', 'Thursday', 'Thursday',
#      'Friday', 'Friday', 'Saturday', 'Saturday'],
#     ['not optimal', 'optimal', 'not optimal', 'optimal', 'not optimal', 'optimal', 'not optimal', 'optimal',
#      'not optimal', 'optimal', 'not optimal', 'optimal', 'not optimal', 'optimal']]
#
# tuples = list(zip(*arrays))
# index = pd.MultiIndex.from_tuples(tuples)
# my_array = np.ones((3, 14))
# df = pd.DataFrame(my_array, index=['A', 'B', 'C'], columns=index)
# df.to_csv(('test.csv'))
# # import os
# from sklearn.datasets import load_iris
#
# iris = load_iris()
#
# # Model (can also use single decision tree)
# from sklearn.ensemble import RandomForestClassifier
#
# model = RandomForestClassifier(n_estimators=10)
#
# # Train
# model.fit(iris.data, iris.target)
# # Extract single tree
# estimator = model.estimators_[5]
#
# from sklearn.tree import export_graphviz
#
# # Export as dot file
# export_graphviz(estimator, out_file='tree.dot',
#                 feature_names=iris.feature_names,
#                 class_names=iris.target_names,
#                 rounded=True, proportion=False,
#                 precision=2, filled=True)
#
# # Convert to png using system command (requires Graphviz)
# from subprocess import call
#
# call(['dot', '-Tpng', 'tree.dot', '-o', 'tree.png', '-Gdpi=600'])
#
# # Display in jupyter notebook
# from IPython.display import Image
#
# Image(filename='tree.png')
# import datetime
# # import pandas as pd
# #
# #
# # df = pd.read_csv('csv_files/results.csv')
# #
# # y = df.as_matrix(columns=df.columns[14:15])
# # y_2 = y.ravel()
# # print('exit')
# #
# # # New series
# # s= pd.Series({'g':6})
# # print(len(s))
#
#
# Get coulmns by index
# df = pd.DataFrame({'month': [1, 4, 7, 10],
#                    'year': [2012, 2014, 2013, 2014],
#                    'sale': [55, 40, 84, 31]})
# print(df.columns[0])
# df_2 =pd.DataFrame(columns= df.columns[1:])
# print(df_2)
#
# # Date to Day
# # import datetime
# # # from datetime import date
# # # date=str(input('Enter the date(for example:09 02 2019):'))
# # date= '10_7_19'
# # day, month, year = date.split('_')
# # day_name = datetime.date(int(year), int(month), int(day))
# # print(day_name.strftime("%A"))
