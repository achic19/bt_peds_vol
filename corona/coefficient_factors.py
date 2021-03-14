import os
import time

import pandas as pd

from avarage_speed_calc import AverageSpeedCalc
from fromBTtoPedsFlow import BTtoPesdFlow


def test_real_count_link():
    # this file check the stability of the links ( weather they work every daty)
    summery_file = pd.read_csv('coefficient _factors/summery.csv')
    co_file = pd.read_csv('coefficient _factors/utm_ground_measures.csv')
    co_file['popularity'] = co_file.apply(lambda x: summery_file[summery_file['via_to'] == x['via_to']]['sum'].values[0], axis=1)
    co_file.to_csv('coefficient _factors/utm_ground_measures.csv')


def create_folder(bt_file):
    """
    :param bt_file: based on this , a new folder will be created
    :return: progress_folder_path, for
    """
    # the format of the code should be : day_month_year
    new_folder_name = bt_file.replace('.csv', '')
    new_folder_name = str.replace(new_folder_name, '.', '_')
    print('The code run on {}'.format(new_folder_name))
    temp_folder_path = os.path.join(data_path, new_folder_name)
    if not os.path.isdir(temp_folder_path):
        os.makedirs(temp_folder_path)
    return temp_folder_path


def process_tb_data():
    ''' '''
    net_length_file_path = os.path.join(data_path, 'mean_std_bidirectional.csv')
    for i, bt_file in enumerate(['28.10.20.csv', '15.08.19.csv']):
        bt_file_path = os.path.join(data_path, bt_file)
        progress_folder_path = create_folder(bt_file)
        t1 = time.time()
        AverageSpeedCalc(bt_file=bt_file_path,
                                               mean_std_bidirectional_df=net_length_file_path,
                                               data_path=data_path, progress_folder_path=progress_folder_path,
                                               time_for_avg=300,
                                               cal_speed=True, co_factor=True)
        print("Calculation of speed and average speed on bt_file is done in {} seconds".format(time.time() - t1))

        BTtoPesdFlow(workspace=progress_folder_path,
                     season_diff_time=i + 1,
                     penetration_rate=1,
                     speed=0, what_to_run=['detect_pedestrians'])


def process_measurements(measurements_path):
    """"
    :param measurements_path of file
    """
    df = pd.read_csv(measurements_path)
    # Israel timeZone to gmt in unix
    data_time = pd.DatetimeIndex(df['time']).tz_localize(tz='Israel').tz_convert(None)
    df['gmt_time'] = (data_time - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
    df.to_csv('coefficient _factors/utm_ground_measures.csv')


def calc_bt_count(x, dates_file):
    date = str(x['time']).split(' ')[0]
    bt_data = dates_file[date]
    bt_file = bt_data[0]
    same_link_records = bt_file[(bt_file['TOUNITC'] + bt_file['VIAUNITC'] == x['via_to']) |
                                (bt_file['VIAUNITC'] + bt_file['TOUNITC'] == x['via_to'])]
    bt_in_same_time = same_link_records[(same_link_records['LASTDISCOTS'] >= x['gmt_time']) & (
            same_link_records['LASTDISCOTS'] <= x['gmt_time'] + bt_data[1])]
    return bt_in_same_time.shape[0]


def calculate_factor(path, dates_file):
    df = pd.read_csv(path)
    df['bt_count'] = df.apply(lambda x: calc_bt_count(x, dates_file), axis=1)
    test_file = pd.read_csv('coefficient _factors/stat_final_loop_2.csv')
    validate_via_to = list(test_file['via_to'])
    df['validate'] = df.apply(lambda x: x['via_to'] in validate_via_to, axis=1)
    df['coef'] = df['count'] / df['bt_count']
    df.to_csv('coefficient _factors/coff_factors.csv')


if __name__ == '__main__':
    paramters = {'process Tb data': False, 'process measurements': False, 'test_real_count_link': False,
                 'calculate factor': True}

    data_path = 'coefficient _factors'
    if paramters['process Tb data']:
        process_tb_data()
    if paramters['process measurements']:
        process_measurements('coefficient _factors/ground_trouth_count.csv')
    if paramters['test_real_count_link']:
        test_real_count_link()
    if paramters['calculate factor']:
        file_19 = pd.read_csv('coefficient _factors/15_08_19/peds_records.csv')
        file_20 = pd.read_csv('coefficient _factors/28_10_20/peds_records.csv')
        calculate_factor('coefficient _factors/utm_ground_measures.csv',
                         {'8/15/2019': (file_19, 60 * 60), '10/28/2020': (file_20, 60 * 30)})
