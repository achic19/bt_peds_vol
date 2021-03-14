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

parameters = ['BTData_Jun2019.csv']
for file in parameters:
    # create folder if necessary
    folder_name = file.split('.')[0]
    print(folder_name)
    if folder_name == 'BTData_Dec2019_Updated':
        continue
    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)

    # split the file to days
    columns = ['to_delete', 'TOKENS', 'PK_UID', 'MAC', 'FROMUNITC', 'VIAUNITC', 'TOUNITC', 'DESTUNITC',
               'OPENTS',
               'LASTDISCOTS',
               'CLOSETS', 'TOLASTDISCOTS', 'OPENTS_GMT', 'LASTDISCOTS_GMT', 'CLOSETS_GMT', 'TOLASTDISCOTS_GMT',
               'STDCALC', 'AVGCALC', 'SECONDSSTD', 'UNITSSTD', 'ROWSTATUS', 'TRIPTIME']

    if folder_name == 'MAY_23_2020_to_PRESENT':
        columns.pop(2)
    if folder_name == 'BTData_Ocb2019' or folder_name == 'BTData_Oct2019_1-27':
        # df = pd.read_csv(file, header=0,  low_memory=False)
        df = pd.read_csv(file, header=0, names=columns, low_memory=False)
    elif folder_name == 'BTData_Mar2019':
        # df = pd.read_csv(file, converters={'to_delete': right_format})
        df = pd.read_csv(file,encoding= 'unicode_escape', low_memory=False)
    else:
        df = pd.read_csv(file, header=0, names=columns)
        #  df = pd.read_csv(file, header=0)

    if folder_name == 'BTData_Mar2019_test':
        df = df[columns]
    if folder_name != 'MAY_23_2020_to_PRESENT':
        df.drop('to_delete', axis=1, inplace=True)
    print(' {}'.format(df.columns))
    df_new = df[0:10]
    df_new.to_csv(folder_name + '/heading.csv')
    #
    # except Exception:
    #     e = sys.exc_info()[1]
    #     print(e.args[0])
    #     continue
    # timestamp to gmt
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

# readable_time = pd.to_datetime(1581976918, unit='s')
# print(readable_time)
# time_zone = readable_time.tz_localize('GMT')
# print(time_zone)
# time_zone2 = time_zone.tz_convert(tz='Israel')
# print(time_zone2)
# isr_time = str(time_zone2).split('+')[0]
# print(isr_time)
# month = isr_time.split('-')[1]
# print(month)
#
# readable_time = pd.to_datetime(1567197703, unit='s')
# print(readable_time)
# time_zone = readable_time.tz_localize('GMT')
# print(time_zone)
# time_zone2 = time_zone.tz_convert(tz='Israel')
# print(time_zone2)
# print(type(time_zone2))
