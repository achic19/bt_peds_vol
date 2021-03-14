import pandas as pd
df = pd.read_csv('tripsRaw - 2020-08-17T120615.744.csv')
df['via_to'] = df['VIAUNITC'] + df['TOUNITC']
groups = df.groupby('via_to')
for group in groups.groups:
    print(group)
