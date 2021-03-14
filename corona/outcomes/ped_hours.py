import datetime
import os

import matplotlib.pyplot as plt
import pandas as pd

plt.close('all')


def work_with_folder(name):
    "go over the the file in each month in month list of the specified period and year ( determined by name)"
    print(period_dic[period][name])
    # go over all the file in the specified months
    for folder in period_dic[period][name]:
        ped_files_path = os.path.join(data_source_folder, folder)
        for ped_file_path in os.listdir(ped_files_path):
            calculate_avg(ped_file_path, os.path.join(ped_files_path, ped_file_path, 'results.csv'), name.split('_')[1])


def work_with_files(name):
    # work on specific files in period_dic[period][name][month]
    for month in period_dic[period][name].keys():
        print(month)
        for date in period_dic[period][name][month]:
            # find the requires file by matching name
            date = str(date)
            if len(date) == 1:
                date = '0' + date
            path = os.path.join(data_source_folder, month)
            file_template = os.listdir(path)[0].rsplit('_', 1)[0]
            ped_file_path = file_template + '_' + date
            calculate_avg(ped_file_path, os.path.join(path, ped_file_path, 'results.csv'),name.split('_')[1])


def calculate_avg(ped_file_path, path_to_file, year):
    """
    this function calculate for each date avarage for each hour
    :param path_to_file: path to the result file in the specified date
    :return:
    """
    # for each date
    str_list = ped_file_path.split('_')
    new_date = str_list[-1] + '.' + str_list[-2]
    print(new_date)

    ped_file = pd.read_csv(path_to_file, index_col='via_to')
    ped_file.drop(columns='Unnamed: 0', inplace=True)

    # check whether the file is weekend or not
    day_name = datetime.date(int(year), int(str_list[-2]), int(str_list[-1]))
    day = day_name.strftime("%A")
    if day == 'Friday' or day == 'Saturday':
        # save the avarge for each hour for the current date
        weekends[new_date] = ped_file.mean()
    else:
        weekdays[new_date] = ped_file.mean()


# periods defination
data_source_folder = os.path.join(os.path.split(os.getcwd())[0], 'progress_files')
# period_dic = {
#     'quarantine': {'files_2020': {'BTData_Mar2020': list(range(25, 31)),
#                                   'BTData_Apr2020': list(range(1, 8)) + list(range(11, 28))},
#                    'folder_2019': ['BTData_Apr2019']}}
period_dic = {
    'before_corona': {'folder_2020': ['BTData_Feb2020'], 'files_2020': {'BTData_Mar2020': list(range(1, 8))},
                      'folder_2019': ['BTData_Feb2019']},
    'limited_gatherings_100': {'files_2020': {'BTData_Mar2020': list(range(11, 15))},
                               'folder_2019': ['BTData_Mar2019']},
    'limited_gatherings_10': {'files_2020': {'BTData_Mar2020': list(range(15, 25))},
                              'folder_2019': ['BTData_Mar2019']},
    'quarantine': {'files_2020': {'BTData_Mar2020': list(range(25, 31)),
                                  'BTData_Apr2020': list(range(1, 7)) + list(range(11, 28))},
                   'folder_2019': ['BTData_Apr2019']},
    'passover': {'files_2020': {'BTData_Apr2020': list(range(8, 12))},
                 'files_2019': {'BTData_Apr2019': list(range(19, 21))}},
    'independence': {'files_2020': {'BTData_Apr2020': list(range(28, 30))},
                     'files_2019': {'BTData_May2019': list(range(8, 10))}},
    'exit_quarantine': {'files_2020': {'BTData_Apr2020': list(range(30, 31)),
                                       'BTData_May2020': list(range(1, 27))},
                        'folder_2019': ['BTData_May2019']},
    'toward_2_wave': {'folder_2020': ['BTData_Jun2020', 'BTData_Jul2020'],
                      'files_2020': {'BTData_May2020': list(range(27, 32))},
                      'folder_2019': ['BTData_Jun2019', 'BTData_Jul2019']}}

for period in period_dic.keys():
    print(period)
    weekdays = pd.DataFrame(index=list(map(str, range(0, 24))))
    weekends = pd.DataFrame(index=list(map(str, range(0, 24))))
    # save a avarage for 2019 corresponding period
    if 'folder_2019' in period_dic[period]:
        work_with_folder('folder_2019')
    else:
        work_with_files('files_2019')

    weekdays_19 = weekdays.mean(axis=1)
    weekends_19 = weekends.mean(axis=1)


    weekdays = pd.DataFrame(index=list(map(str, range(0, 24))))
    weekends = pd.DataFrame(index=list(map(str, range(0, 24))))
    if 'folder_2020' in period_dic[period]:
        work_with_folder('folder_2020')
    if 'files_2020' in period_dic[period]:
        work_with_files('files_2020')
    weekdays_20 = weekdays.mean(axis=1)
    weekends_20 = weekends.mean(axis=1)

    if period =='passover':
        final = pd.concat([weekends_19,weekdays_20], axis=1, sort=False).rename(columns={0:2019,
                                                                                                  1:2020})
        final.to_csv(os.path.join('ped_hours',period +'.csv'))
        final.plot(title=period)
        plt.savefig(os.path.join('ped_hours',period +'.png'))

    elif period== 'independence':
        weekdays_final = pd.concat([weekdays_19,weekdays_20], axis=1, sort=False).rename(columns={0:2019,
                                                                                                  1:2020})
        weekdays_final.to_csv(os.path.join('ped_hours',period +'.csv'))
        weekdays_final.plot(title=period )
        plt.savefig(os.path.join('ped_hours',period +'.png'))
    else:
        weekdays_final = pd.concat([weekdays_19,weekdays_20], axis=1, sort=False).rename(columns={0:2019,
                                                                                                  1:2020})
        weekends_final = pd.concat([weekends_19,weekends_20], axis=1, sort=False).rename(columns={0:2019,
                                                                                                  1:2020})
        weekdays_final.to_csv(os.path.join('ped_hours',period +'_weekdays.csv'))
        weekends_final.to_csv(os.path.join('ped_hours',period +'_weekends.csv'))
        weekdays_final.plot(title=period +'_weekdays' )
        plt.savefig(os.path.join('ped_hours',period +'_weekdays.png'))
        weekends_final.plot(title=period + '_weekends')
        plt.savefig(os.path.join('ped_hours',period +'_weekends.png'))

