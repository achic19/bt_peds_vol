import os

import pandas as pd


def right_format(x):
    try:
        return x
    except UnicodeDecodeError:
        return str(x)


directory = os.getcwd()
# os.path.realpath(__file__)

os.chdir(directory)
# What to run  - all files in the folder or specific files as in a list
# parameters = [glob.glob("*.csv"),['BTData_Mar2019.csv','BTData_Apr2019.csv','']]
file = 'BTData_Feb2020.csv'

# create folder if necessary
folder_name = 'BTData_Feb2020'
print(folder_name)
# split the file to days
columns = ['to_delete', 'TOKENS', 'PK_UID', 'MAC', 'FROMUNITC', 'VIAUNITC', 'TOUNITC', 'DESTUNITC',
           'OPENTS',
           'LASTDISCOTS',
           'CLOSETS', 'TOLASTDISCOTS', 'OPENTS_GMT', 'LASTDISCOTS_GMT', 'CLOSETS_GMT', 'TOLASTDISCOTS_GMT',
           'STDCALC', 'AVGCALC', 'SECONDSSTD', 'UNITSSTD', 'ROWSTATUS', 'TRIPTIME']



# df = pd.read_csv(file, converters={'to_delete': right_format})
# df = pd.read_csv(file,nrows=1247162,encoding= 'unicode_escape', header=0, names=columns)
# skip_rows= list(range(1247162,1247208))
df = pd.read_csv(file,header=0, names=columns,error_bad_lines=False)
# df = pd.read_csv(file, header=0, names=columns)
df.drop('to_delete', axis=1, inplace=True)
print(' {}'.format(df.columns))
print('start to calculate time')
# except Exception:
#     e = sys.exc_info()[1]
#     print(e.args[0])
#     continue
#timestamp to gmt
df['OPENTS_GMT'] = pd.to_datetime(df['OPENTS'], unit='s')
df['LASTDISCOTS_GMT'] = pd.to_datetime(df['LASTDISCOTS'], unit='s')
df['CLOSETS_GMT'] = pd.to_datetime(df['CLOSETS'], unit='s')
df['TOLASTDISCOTS_GMT'] = pd.to_datetime(df['TOLASTDISCOTS'], unit='s')
print('timestamp to gmt is finished')
# gmt to Israel timeZone
data_time = pd.DatetimeIndex(df['OPENTS_GMT']).tz_localize('GMT').tz_convert(tz='Israel')
df['isr_time'] = data_time
#  To eliminate the difference hour the column converted to string and split it
time_as_str = df['isr_time'].apply(str)
df['isr_time'] = time_as_str.str.split('+', expand=True)
df['date'] = data_time.date
print('gmt to Israel timeZone')
for i, (name, group) in enumerate(df.groupby('date')):
    group.to_csv(folder_name + '/file{}.csv'.format(name))
    print(str(name))

print("all the files are process")

