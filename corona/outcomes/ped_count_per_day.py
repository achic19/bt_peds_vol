import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
plt.close('all')
# parameters
data_source_folder = os.path.join(os.path.split(os.getcwd())[0], 'progress_files')
folder_to_work_on = ['BTData_Feb2020', 'BTData_Mar2020', 'BTData_Apr2020', 'BTData_May2020', 'BTData_Jun2020',
                     'BTData_Jul2020']
# folder_to_work_on = ['BTData_Mar2020', 'BTData_Apr2020']
ped_dict_weekday= {}
ped_dict_weekend= {}
links_list = list(pd.read_csv('links_file.csv')['link_names'])
for folder in folder_to_work_on:
    print(folder)
    ped_files_path = os.path.join(data_source_folder, folder)
    for ped_file_path in os.listdir(ped_files_path):
        # for each date
        str_list = ped_file_path.split('_')
        new_date = str_list[-1] + '.' + str_list[-2]
        print(new_date)

        ped_file = pd.read_csv(os.path.join(ped_files_path, ped_file_path, 'results.csv'), index_col='via_to')
        ped_file.drop(columns='Unnamed: 0',inplace=True)

        # check whether the file is weekend or not
        day_name = datetime.date(2020, int(str_list[-2]), int(str_list[-1]))
        day = day_name.strftime("%A")
        # calculate the number of pedestrians
        if day == 'Friday' or day == 'Saturday':
            ped_file_temp = ped_file.loc[:,list(map(str, range(7, 24)))]
            # print(ped_file_temp.shape[0])
            ped_file_temp = ped_file_temp[ped_file_temp.index.isin(links_list)]
            # print(ped_file_temp.shape[0])
            ped_dict_weekend[new_date] = ped_file_temp.mean().mean()
        else:
            ped_file_temp = ped_file.loc[:, list(map(str, range(6, 24)))]
            # print(ped_file_temp.shape[0])
            ped_file_temp = ped_file_temp[ped_file_temp.index.isin(links_list)]
            # print(ped_file_temp.shape[0])
            ped_dict_weekday[new_date] = ped_file_temp.mean().mean()

for ped_dict,time in [(ped_dict_weekday,'weekday'),(ped_dict_weekend,'weekend')]:
    df = pd.DataFrame(data=ped_dict.values(), index=list(ped_dict.keys()), columns=['count'])
    df.to_csv('ped_count_per_day/' + time + '_ped_count_per_day_mean_days_hours_same_link.csv')

    df.plot()
    plt.savefig('ped_count_per_day/' + time + '_ped_count_per_day_mean_days_hours_same_link.png')


