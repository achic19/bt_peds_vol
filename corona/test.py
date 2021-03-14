import os
import pandas as pd
df = r'D:\Users\OneDrive - Technion\PhD\research\big_data_padestrian_flow\data\progress_files\4_8_19\results.csv'
df = pd.read_csv(df)
one_way_link = pd.read_csv('one_way.csv')
for index, row in one_way_link.iterrows():
    if row['VIA'] > row['TO']:
        one_way_link.at[index, 'via_to'] = row['TO'] + row['VIA']
    else:
        one_way_link.at[index, 'via_to'] = row['VIA'] + row['TO']
validate_via_to = list(one_way_link['via_to'])
# df.loc[df['via_to'].isin(validate_via_to)].iloc[:,2:] = (df.loc[df['via_to'].isin(validate_via_to)].iloc[:,2:]) *2

str_time= list(map(str, list(range(24))))
df.loc[df['via_to'].isin(validate_via_to),str_time ] =df.loc[df['via_to'].isin(validate_via_to),str_time ]*2

df.to_csv("results2.csv")

