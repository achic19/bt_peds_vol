import os
import time

from avarage_speed_calc import AverageSpeedCalc
from fromBTtoPedsFlow import BTtoPesdFlow
from prepare_machine_learning import build_data_machine_learning


def create_folder():
    """
    :return: progress_folder_path, for
    """
    # the format of the code should be : day_month_year
    new_folder_name = bt_file.replace('.csv', '')
    new_folder_name = str.replace(new_folder_name, '.', '_')
    print('The code run on {}'.format(new_folder_name))
    temp_folder_path = os.path.join(progress_files_path, new_folder_name)
    if not os.path.isdir(temp_folder_path):
        os.makedirs(temp_folder_path)
    return temp_folder_path


# parameters, If necessary don't forget to change 'mean_std_bidirectional.csv' file
# Run on specific folder or all of them
# 'avarage_speed_calc','find_number_of_peds_per_link_per_hour'
parameters = {'time_for_avg': 300,
              'pen_rate': 3.36,
              'folder_to_run_on': ['all'],  # the date format is day_month_year
              'which_class_to_run': ['avarage_speed_calc'],
              'cal_speed': True}

find_number_parameters = {
    'season_diff_time': 3,
    'speed': 0.833
}

# these path is necessary for several class implementations
data_path = os.path.join(os.path.split(os.path.split(__file__)[0])[0], 'data')
progress_files_path = os.path.join(data_path, 'progress_files')

# code for avarage_speed_calc class
if 'avarage_speed_calc' in parameters['which_class_to_run']:

    # prepare data to work on : define bt_files_path and progress_files_path
    bt_files_path = os.path.join(data_path, 'raw_big_data')

    net_length_file_path = os.path.join(data_path, 'mean_std_bidirectional.csv')

    # create progress_folder (if needed) to store the results and process the data
    for bt_file in os.listdir(bt_files_path):
        if parameters['folder_to_run_on'][0] != 'all' and bt_file not in parameters['folder_to_run_on']:
            continue
        else:
            print(bt_file)
            bt_file_path = os.path.join(bt_files_path, bt_file)
            progress_folder_path = create_folder()
            t1 = time.time()
            bt_file_with_speeds = AverageSpeedCalc(bt_file=bt_file_path,
                                                   mean_std_bidirectional_df=net_length_file_path,
                                                   data_path=data_path, progress_folder_path=progress_folder_path,
                                                   time_for_avg=parameters['time_for_avg'],
                                                   cal_speed=parameters['cal_speed'])
            print("Calculation of speed and average speed on bt_file is done in {} seconds".format(time.time() - t1))

# code for find_number_of_peds_per_link_per_hour class
if 'find_number_of_peds_per_link_per_hour' in parameters['which_class_to_run']:

    # run over all or parts of the folders to apply the class methods on
    for folder in os.listdir(progress_files_path):
        if parameters['folder_to_run_on'][0] != 'all' and folder not in parameters['folder_to_run_on']:
            continue
        else:
            print(folder)
            bt_file_path = os.path.join(progress_files_path, folder)
            if folder in ['21_11_19', '19_02_20']:
                find_number_parameters['season_diff_time'] = 2
            BTtoPesdFlow(workspace=bt_file_path,
                         season_diff_time=find_number_parameters['season_diff_time'],
                         penetration_rate=parameters['pen_rate'],
                         speed=find_number_parameters['speed'])
            if parameters['folder_to_run_on'][0] != 'all' and len(parameters['folder_to_run_on']) == 1:
                break
            find_number_parameters['season_diff_time'] = 3

if 'prepare_machine_learning' in parameters['which_class_to_run']:
    build_data_machine_learning(progress_files_path)

