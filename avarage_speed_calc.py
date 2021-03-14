import os
from _datetime import datetime

import arcpy
import pandas as pd


class AverageSpeedCalc:

    def __init__(self, bt_file, mean_std_bidirectional_df, progress_folder_path, time_for_avg,
                 cal_speed=True, co_factor=False):
        """

        :param bt_file: path to BT file to calculate speed and average speed
        :param mean_std_bidirectional_df: csv file for links and their net length
        :param progress_folder_path: to st
        :param time_for_avg: fpr average calculation ,from the group  collect only the records
         had been in last 300 seconds in the link before the current record  came up
         :param cal_avg_speed: if false , don't run calc_avg_speed ( time consuming method )
         :param co_factor: to handle new files with a different relation to the source
        :return:
        """
        # CSV files to dataframe

        mean_std_bidirectional_df = pd.read_csv(mean_std_bidirectional_df)
        self.progress_folder_path = progress_folder_path
        self.time_for_avg = time_for_avg
        self.co_factor = co_factor
        # Filter data ( use only records having net length) and calculate speed and average speed for each record
        if cal_speed:
            bt = self.join_data(bt_file)
            self.bt = self.calculate_speed(bt, mean_std_bidirectional_df)
        else:
            self.bt = pd.read_csv(os.path.join(self.progress_folder_path, 'speed.csv'))
        self.bt = self.calc_avg_speed()

    def join_data(self, bt_file):
        """
        :param bt_file: the BT raw file
        :return: BT raw file that includes only records related to our network
        """
        print("initiate join_data def  - Work only with links within the experiment area.")
        # from feature class to dataframe format
        via_to = list()
        shape_length = list()
        cursor = arcpy.da.SearchCursor('links_network.shp', ['via_to', 'Shape_Leng'])
        for row in cursor:
            via_to.append(row[0])
            shape_length.append(row[1])
        df_network = pd.DataFrame({'via_to': [], 'Shape_Length': []})
        df_network['via_to'] = via_to
        df_network['Shape_Length'] = shape_length

        # Merge feature class and csv file
        all_bt_file = pd.read_csv(bt_file)
        print("the number of records in the source file is {}".format(all_bt_file.shape[0]))
        all_bt_file['via_to'] = all_bt_file['VIAUNITC'] + all_bt_file['TOUNITC']
        bt = pd.merge(all_bt_file, df_network, on=['via_to'], how='inner')
        if self.co_factor:
            bt.to_csv(os.path.join(self.progress_folder_path, 'join.csv'))
        else:
            bt.to_csv(os.path.join(self.progress_folder_path, 'join.csv'))
        print("the number of records related to our network is {}".format(bt.shape[0]))
        print("join_data def is done")
        return bt

    def calculate_speed(self, join_df, mean_std_bidirectional_df):
        """
         Filter data ( use only records having net length) and calculate speed  speed for each record
        :param join_df: BT raw file that includes only records related to our network
        :param mean_std_bidirectional_df: csv file with links and net average length
        :return:
        """
        print(
            "initiate join_data def  - Filter data "
            "( use only records having net length) and calculate speed  speed for each record")
        # store only records belongs to links in mean_std_bidirectional_df file
        rel_links = join_df.loc[(join_df['via_to'].isin(mean_std_bidirectional_df['via_to']))]
        rel_links.to_csv(os.path.join(self.progress_folder_path, 'rel_links.csv'))
        print(
            "the number of records belongs to links in mean_std_bidirectional_df file is {}".format(rel_links.shape[0]))

        # Build dictionary of links and length
        my_dict = {row[2]: row[3] for row in mean_std_bidirectional_df.values}
        my_dict_std = {row[2]: row[4] for row in mean_std_bidirectional_df.values}
        rel_links['net_link'] = ''
        rel_links['std_speed'] = ''
        for index, row in rel_links.iterrows():
            if row['CLOSETS'] - row['LASTDISCOTS'] > 0:
                rel_links.at[index, 'net_link'] = my_dict[row['via_to']]
                rel_links.at[index, 'std_net_link'] = my_dict_std[row['via_to']]
                rel_links.at[index, 'speed'] = my_dict[row['via_to']] / (row['CLOSETS'] - row['LASTDISCOTS'])
                rel_links.at[index, 'std_speed'] = my_dict_std[row['via_to']] / (row['CLOSETS'] - row['LASTDISCOTS'])
            else:
                rel_links.at[index, 'speed'] = -1000
        # drop records without speed
        rel_links = rel_links.drop(rel_links[rel_links['speed'] == -1000].index)
        rel_links.to_csv(os.path.join(self.progress_folder_path, 'speed.csv'))

        print("calculate_speed def is done")
        return rel_links

    def calc_avg_speed(self):

        """
        For each record in each group find all the other records that was in
             the same link in the same time ( -300 sec) and calculate average and standard deviation
        :param penetration_rate: 4.545 in Tsmart system
        :return: database with speed and average speed
        """
        print(
            "initiate calc_avg_speed def  -For each record in each group find all the other records that was in\
             the same link in the same time ( -300 sec) and calculate average and standard deviation ")

        filtered_db = self.bt
        # Calc our trip time, speed and average speed
        filtered_db.set_index('PK_UID', inplace=True, drop=False)
        filtered_db['avarage_spd'] = ''
        filtered_db['avarage_spd_10800'] = ''

        filtered_db['std_spd_avg'] = ''
        filtered_db['num_of_recs'] = ''

        # For each record in each group find all the other records that was in the same link in the same time
        # ( -300 sec) and
        #  calculate avarage and standard deviation
        # group by link name regardless direction
        gk = filtered_db.groupby('via_to')
        number_of_groups = len(gk)
        print('In {} ,the number of groups are {} which start at {}'.format('test', number_of_groups, datetime.now()))
        for i, group_name in enumerate(filtered_db.via_to.unique()):
            print("Progress {:2.1%}".format(i / number_of_groups))

            group = gk.get_group(group_name)

            for index, record in group.iterrows():
                pk_id = record['PK_UID']
                # In the next rows the code count the number of records
                # in the current moment ('CLOSETS') on the link ( the worst case) for a specific record

                record_LASTDISCOTS = record['LASTDISCOTS']
                result = group.loc[(record_LASTDISCOTS - group['LASTDISCOTS'] < self.time_for_avg) & (
                        record_LASTDISCOTS - group['LASTDISCOTS'] >= 0)]
                result_10800 = group.loc[(record_LASTDISCOTS - group['LASTDISCOTS'] < 10800) & (
                        record_LASTDISCOTS - group['LASTDISCOTS'] >= 0)]
                if result_10800.shape[0] > 1:
                    filtered_db.at[pk_id, 'avarage_spd'] = result.speed.mean()
                    filtered_db.at[pk_id, 'avarage_spd_10800'] = result_10800.speed.mean()
                    # filtered_db['std_spd_avg'].loc[filtered_db['PK_UID'] == pk_id] = math.sqrt(
                    #     (result_10800['speed'] ** 2).sum()) / result_10800.shape[0]
                    filtered_db.at[pk_id, 'std_spd_avg'] = result_10800.speed.std()
                    filtered_db.at[pk_id, 'num_of_recs'] = result_10800.shape[0]
                else:
                    filtered_db.at[pk_id, 'avarage_spd_10800'] = result_10800.speed.mean()
                    filtered_db.at[pk_id, 'avarage_spd'] = result_10800.speed.mean()
                    filtered_db.at[pk_id, 'std_spd_avg'] = 0
                    filtered_db.at[pk_id, 'num_of_recs'] = 1
        # save only file with calculated avarage_spd
        filtered_db.reset_index(inplace=True, drop=True)
        filtered_db.to_csv(
            os.path.join(self.progress_folder_path, 'avarage_spd.csv'))
        print("calc_avg_speed def is done")
        print(datetime.now())
        return filtered_db
