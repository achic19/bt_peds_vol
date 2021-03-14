"""
In this file:
1. the code uploads the current model
2. create a csv file which store for each time in every day number of optimal segments and non - optimal segments
"""
import pickle

import numpy as np
import pandas as pd

# prepare data
df = pd.read_csv('csv_files/all_osm_data.csv')
# this array help to build multiIndex column
arrays = [
    ['Sunday', 'Sunday', 'Monday', 'Monday', 'Tuesday', 'Tuesday', 'Wednesday', 'Wednesday', 'Thursday', 'Thursday',
     'Friday', 'Friday', 'Saturday', 'Saturday'],
    ['not optimal', 'optimal', 'not optimal', 'optimal', 'not optimal', 'optimal', 'not optimal', 'optimal',
     'not optimal', 'optimal', 'not optimal', 'optimal', 'not optimal', 'optimal']]

tuples = list(zip(*arrays))
index = pd.MultiIndex.from_tuples(tuples)
my_array = np.ones((24, 14))

# load the model from disk
filename = 'finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

# Upload and prepare  data

for i in range(7):
    k = 2 * i
    for j in range(24):
        df['time'] = j
        df['day'] = i + 1
        X = df.to_numpy()
        # make a prediction
        ynew = loaded_model.predict(X)
        my_array[j, k] = np.count_nonzero(ynew == 1)
        my_array[j, k + 1] = np.count_nonzero(ynew == 2)
        print(my_array[j])

df = pd.DataFrame(my_array, columns=index)
df.to_csv('csv_files/all_data.csv')
