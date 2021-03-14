import datetime
import os

import pandas as pd


def build_data_machine_learning(folder):
    """
    :param folder:  folder path contains all the data on pedestrian flow for different dates
    :return:
    """

    # Upload features table
    feature_class_data = pd.read_csv(r'csv_files/links_network_with_features.csv')
    # pandas drop columns using list of column names
    feature_class_data.drop(['OBJECTID', 'Join_Count', 'TARGET_FID', 'LENGTH', 'Shape_Length'], axis=1, inplace=True)
    #  empty list to store all the joined dataframes
    frames = []
    # Dictionary day as name to day as number
    days = {"Monday": 2, "Tuesday": 3, "Wednesday": 4, "Thursday": 5, "Friday": 6, "Saturday": 7, "Sunday": 1}
    # For each pedestrian level file for each date
    for date_folder in os.listdir(folder):
        #   Join file to features table
        file_path = os.path.join(folder, date_folder, 'pedestrian_flow.csv')
        flow_data = pd.read_csv(file_path)
        join_file = pd.merge(feature_class_data, flow_data, on=['via_to'], how='inner')
        #   if there is a link in pedestrian level file missing in features table
        #   raise Exception("Link is missing in feature_class_data")
        if flow_data.shape[0] != join_file.shape[0]:
            raise Exception("Link is missing in feature_class_data")
        #   Add new column with a day name as a number
        day, month, year = date_folder.split('_')
        day_name = datetime.date(int(year), int(month), int(day))
        join_file['day'] = days[day_name.strftime("%A")]
        join_file['date'] = date_folder
        # Delete unnecessary field
        join_file.drop('Unnamed: 0', axis=1, inplace=True)
        #   Append the result
        frames.append(join_file)

    # empty list to store all the updated dataframes
    rows_list = []

    # For each dataframe in dataframes list; for each row; for each hour:
    #   build new series - features , hour, day, ped flow ( for test -date and  link name )
    #   Convert it back to dataframe ( with one row) and append it to a ist
    for frame in frames:
        print(frame.at[0, 'date'])
        for row in frame.iterrows():
            for j in range(24):
                temp_row = [row[1][1:12],
                            pd.Series({'time': j, 'day': row[1][len(row[1]) - 2], 'ped_flow': row[1][12 + int(j)],
                                       'date': row[1][len(row[1]) - 1], 'via_to': row[1][0]})]
                temp_row = pd.concat([temp_row[0], temp_row[1]])
                temp_row = pd.DataFrame(temp_row).transpose()
                rows_list.append(temp_row)

    # Concatenate all to one dataframe
    results = pd.concat(rows_list, ignore_index=True, sort=False)
    results.to_csv('csv_files/results.csv')
