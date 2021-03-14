import datetime
import os

import matplotlib.pyplot as plt
import pandas as pd

# periods defination
data_source_folder = os.path.join(os.getcwd(), 'ped_hours_links')
# go over all folders
for folder in os.listdir(data_source_folder):
    print(folder)
    data_source_folder_2 = os.path.join(data_source_folder, folder)
    # go over all the weekend/weekdays folder
    for folder_2 in os.listdir(data_source_folder_2):
        ratio =pd.DataFrame(columns=['2019','2020','ratio'])
        data_source_folder_3 = os.path.join(data_source_folder_2, folder_2)
        # if ratio file is already exist
        if os.path.isfile(os.path.join(data_source_folder_3, 'ratio.csv')):
            os.remove(os.path.join(data_source_folder_3, 'ratio.csv'))
        for file in os.listdir(data_source_folder_3):
            if file.endswith(".csv") :
                csv_file_path = os.path.join(data_source_folder_3, file)
                ped_file = pd.read_csv(csv_file_path)
                # get link name
                link_name = file.split('_')[1].split('.')[0]
                print(link_name)
                data_sum =list(ped_file.sum(axis=0))
                data_to_add = data_sum[1:] + [data_sum[2]/data_sum[1]*100]
                ratio.loc[link_name,:] = data_to_add
        ratio.to_csv(os.path.join(data_source_folder_3, 'ratio.csv'))



