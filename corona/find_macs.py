import pandas as pd

# known records
# achituv -
mac_to_test = 'FD2C6017D58D'
df = pd.read_csv('BTData_September2020/tripsRaw - 2020-09-12.csv')

sum_df = pd.DataFrame(index=df['MAC'].unique())
sum_df['agg'] = 0

df['via_to'] = df['VIAUNITC'] + df['TOUNITC']
mac_df = df[df['MAC'] == mac_to_test]
print(mac_to_test.shape[0])
# iterate over:
for index, row in mac_df.iterrows():
    via_to = row['via_to']
    time = row['LASTDISCOTS']
    temp_df = df[(df['MAC'] != mac_to_test) & (df['via_to'] == via_to) & (abs(df['LASTDISCOTS'] - time) < 60)]
    for index, row in temp_df.iterrows():
        sum_df.at[row['MAC'], 'agg'] += 1
    # print(via_to)
    # print(time)
    # print(temp_df['MAC'])
    # print(temp_df['LASTDISCOTS'] -time)
sum_df.to_csv('BTData_September2020/find_mac120920.csv')
