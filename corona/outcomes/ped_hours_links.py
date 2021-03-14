import datetime
import os

import matplotlib.pyplot as plt
import pandas as pd


def work_with_folder(name, link=False):
    '''
    calculate for each date average
    :param name: year
    :param link: for extract average for specific link
    :return:
    '''
    print(period_dic[period][name])
    # go over all the file in the specified months
    for folder in period_dic[period][name]:
        ped_files_path = os.path.join(data_source_folder, folder)
        for ped_file_path in os.listdir(ped_files_path):
            calculate_avg(ped_file_path, os.path.join(ped_files_path, ped_file_path, 'results.csv'), name.split('_')[1],
                          link)


def work_with_files(name, link=False):
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
            calculate_avg(ped_file_path, os.path.join(path, ped_file_path, 'results.csv'), name.split('_')[1], link)


def calculate_avg(ped_file_path, path_to_file, year, link):
    """
    this function calculate for each date avarage for each hour
    :param path_to_file: path to the result file in the specified date
    :return:
    """
    # for each date
    str_list = ped_file_path.split('_')
    new_date = str_list[-1] + '.' + str_list[-2]
    if not link:
        print(new_date)

    ped_file = pd.read_csv(path_to_file, index_col='via_to')
    ped_file.drop(columns='Unnamed: 0', inplace=True)

    # check whether the file is weekend or not
    day_name = datetime.date(int(year), int(str_list[-2]), int(str_list[-1]))
    day = day_name.strftime("%A")
    if link == False:
        if day == 'Friday' or day == 'Saturday':
            # save the avarge for each hour for the current date
            frame_weekends.append(pd.DataFrame(ped_file.mean(axis=1), columns=[new_date]))
        else:
            frame_weekdays.append(pd.DataFrame(ped_file.mean(axis=1), columns=[new_date]))
    else:
        if not link in ped_file.index:
            return
        if time == 'weekends' and (day == 'Friday' or day == 'Saturday'):
            # save the avarge for each hour for the current date
            days.loc[new_date] = ped_file.loc[link]
        if (time == 'weekdays' and (day != 'Friday' and day != 'Saturday')) or (period == 'passover'):
            days.loc[new_date] = ped_file.loc[link]


def create_folder():
    folder_name = os.path.join('ped_hours_links', period)
    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)
    for name in ['weekdays', 'weekends']:
        folder_name = os.path.join('ped_hours_links', period, name)
        if not os.path.isdir(folder_name):
            os.makedirs(folder_name)


def finish_results(file1, file2):
    final = pd.concat([file1, file2], axis=1, sort=False).rename(columns={0: 2019,
                                                                          1: 2020})
    days_path = os.path.join('ped_hours_links', period, time, str(i) + '_' + link)
    final.to_csv(days_path + '.csv')
    final.plot(title=str(i) + '_' + link + '_' + time)
    plt.savefig(days_path + '.png')


# periods defination
data_source_folder = os.path.join(os.path.split(os.getcwd())[0], 'progress_files')
# period_dic = {
# #     'quarantine': {'files_2020': {'BTData_Mar2020': list(range(25, 31)),
# #                                   'BTData_Apr2020': list(range(1, 8)) + list(range(11, 28))},
# #                    'folder_2019': ['BTData_Apr2019']}}

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
                      'folder_2019': ['BTData_Jun2019','BTData_Jul2019']}}
for period in period_dic.keys():
    print(period)
    create_folder()
    frame_weekdays = []
    frame_weekends = []
    # save a avarage for 2019 corresponding period
    if 'folder_2019' in period_dic[period]:
        work_with_folder('folder_2019')
    else:
        work_with_files('files_2019')

    if period != 'passover':
        weekdays_19 = pd.DataFrame(pd.concat(frame_weekdays, axis=1).mean(axis=1), columns=['ped_count'])
    if period != 'independence':
        weekends_19 = pd.DataFrame(pd.concat(frame_weekends, axis=1).mean(axis=1), columns=['ped_count'])

    frame_weekdays = []
    frame_weekends = []
    if 'folder_2020' in period_dic[period]:
        work_with_folder('folder_2020')
    if 'files_2020' in period_dic[period]:
        work_with_files('files_2020')

    if period != 'independence' and period != 'passover':
        weekends_20 = pd.DataFrame(pd.concat(frame_weekends, axis=1).mean(axis=1), columns=['ped_count'])
        subtract_weekends = weekends_20.subtract(weekends_19, axis=1).dropna().abs().sort_values(by='ped_count',
                                                                                                 ascending=False).reset_index()

    weekdays_20 = pd.DataFrame(pd.concat(frame_weekdays, axis=1).mean(axis=1), columns=['ped_count'])

    if period != 'passover':
        subtract_weekdays = weekdays_20.subtract(weekdays_19, axis=1).dropna().abs().sort_values(by='ped_count',
                                                                                                 ascending=False).reset_index()
    else:
        subtract_weekdays = weekdays_20.subtract(weekends_19, axis=1).dropna().abs().sort_values(by='ped_count',
                                                                                                 ascending=False).reset_index()
    for time in ('weekdays', 'weekends'):
        if time == 'weekdays':
            links_len = subtract_weekdays.shape[0]
        else:
            links_len = subtract_weekends.shape[0]
        for i in range(links_len):
            if time == 'weekdays':
                link = subtract_weekdays.iloc[i]['index']
            else:
                link = subtract_weekends.iloc[i]['index']
            print(link)
            days = pd.DataFrame(columns=list(map(str, range(0, 24))))

            if 'folder_2019' in period_dic[period]:
                work_with_folder('folder_2019', link)
            else:
                work_with_files('files_2019', link)

            days_19 = days.mean()

            days = pd.DataFrame(columns=list(map(str, range(0, 24))))
            if 'folder_2020' in period_dic[period]:
                work_with_folder('folder_2020', link)
            if 'files_2020' in period_dic[period]:
                work_with_files('files_2020', link)

            days_20 = days.mean()
            finish_results(days_19, days_20)
            plt.close('all')
        if period == 'passover' or period == 'independence':
            break
