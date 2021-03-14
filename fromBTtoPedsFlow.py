import os

import pandas as pd


class BTtoPesdFlow:
    def __init__(self, workspace, penetration_rate,what_to_run='all'):
        """

        :param workspace: This path will store the BT file and
        :param penetration_rate : the ratio between the real number of users to those detected by the Tsmart
        :return:
        """
        self.workspace_progress = workspace
        bt_file = pd.read_csv(os.path.join(workspace, 'avarage_spd.csv'))
        if 'detect_pedestrians' in what_to_run or what_to_run=='all':
            self.peds_db = self.detect_pedestrians(bt_file)
        if 'find_number_of_peds_per_link_per_hour' in what_to_run or what_to_run=='all':
            self.find_number_of_peds_per_link_per_hour(penetration_rate)

    def detect_pedestrians(self, bt_file):
        """
        Detect pedesrtrins based on the following rules: select the records with speed <1.5  and average speed >1.5 or
         l/15>4.545n which means no congestion
        :param bt_file: bt file to detect_pedestrians
        :return: file only with pedestrian
        """
        print("initiate detect_pedestrians def  - Detect pedestrians records in the BT files")
        # 	congestion if in the  current moment for a specific link  :  l/15 < 4.545n ('cars_links_now')
        size = bt_file.shape[0]
        k_s = 1.1
        k_a_s = 1

        bt_file["std_speed"].fillna(0, inplace=True)  # replacing nan values in std_speed with zero
        size = bt_file.shape[0]
        our_result = bt_file.loc[bt_file['speed'] - k_s * bt_file['std_speed'] <= 1.5]
        our_result = our_result.loc[bt_file['avarage_spd'] > bt_file['avarage_spd_10800'] - k_a_s * bt_file['std_spd_avg']]
        new_size = our_result.shape[0]
        print("the number of pedestrian records  is {} which is {}% out of all records".format(new_size,
                                                                                               new_size / size * 100))
        print("detect_pedestrians def is done")
        our_result.to_csv(os.path.join(self.workspace_progress, 'peds_records.csv'))
        return our_result

    def find_number_of_peds_per_link_per_hour(self, penetration_rate):
        """
        this methods generate a table ( rows - links , columns - hours values - number of pedestrians)
        :param penetration_rate : the ratio between the real number of users to those detected by the Tsmart
        :return: dataframe object with number_of_peds_per_link_per_hour
        """
        # Make it one directional by change the “via_to” field (if necessary) to smaller first in TB file
        for index, row in self.peds_db.iterrows():
            if row['VIAUNITC'] > row['TOUNITC']:
                self.peds_db.at[index, 'via_to'] = row['TOUNITC'] + row['VIAUNITC']
        self.peds_db.to_csv(os.path.join(self.workspace_progress, 'peds_records_reverse.csv'))

        # Work only with necessary fields
        new_pd = self.peds_db[['via_to', 'CLOSETS_GMT']]

        # Take from the field ['CLOSETS_GMT'] the hour (+3 ) in the summer and save it back into ['CLOSETS_GMT'] field

        new_pd['CLOSETS_GMT_isr'] = pd.DatetimeIndex(new_pd['CLOSETS_GMT']).tz_localize('GMT').tz_convert(tz='Israel').hour
        # Group by 'via_to' and 'CLOSETS_GMT' and count the number in each group
        # Unstack so the values in 'CLOSETS_GMT' fields (0-23) will be in column.
        df = (new_pd.reset_index().groupby(['via_to', 'CLOSETS_GMT_isr'])['CLOSETS_GMT_isr'].aggregate(
            'count') * penetration_rate).unstack().fillna(0).reset_index()

        # Update count for one way links
        one_way_link = pd.read_csv('one_way.csv')
        for index, row in one_way_link.iterrows():
            if row['VIA'] > row['TO']:
                one_way_link.at[index, 'via_to'] = row['TO'] + row['VIA']
            else:
                one_way_link.at[index, 'via_to'] = row['VIA'] + row['TO']
        validate_via_to = list(one_way_link['via_to'])
        str_time = list(df.columns[1:])
        df.loc[df['via_to'].isin(validate_via_to), str_time] = df.loc[df['via_to'].isin(validate_via_to), str_time] * 2
        df.to_csv(os.path.join(self.workspace_progress, "results.csv"))
        print('find_number_of_peds_per_link_per_hour is done')
