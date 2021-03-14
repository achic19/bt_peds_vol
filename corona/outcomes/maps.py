import datetime
import os
import pandas as pd



def work_with_folder(name):
    "go over the the file in each month in month list of the specified period and year ( determined by name)"
    print(period_dic[period][name])
    # go over all the file in the specified months
    for folder in period_dic[period][name]:
        ped_files_path = os.path.join(data_source_folder, folder)
        for ped_file_path in os.listdir(ped_files_path):
            calculate_avg(ped_file_path, os.path.join(ped_files_path, ped_file_path, 'results.csv'))


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
            calculate_avg(ped_file_path, os.path.join(path, ped_file_path, 'results.csv'))

def join():
    # Import system modules
    import arcpy
    # Set environment settings
    arcpy.env.workspace = os.getcwd()
    arcpy.env.qualifiedFieldNames = False

    file_path = os.path.join('maps',period)
    if os.path.exists(file_path + '.shp'):
        for item in ['.shp', '.shx', '.cpg', '.dbf', '.prj']:
            os.remove(file_path + item)



    # Set local variables

    joinTable = file_path + '.csv'
    joinField = "via_to"
    outFeature = file_path + '.shp'

    # Join the feature layer to a table
    veg_joined_table = arcpy.AddJoin_management(inFeatures, joinField, joinTable, joinField,join_type='KEEP_COMMON')

    # Copy the layer to a new permanent feature class
    arcpy.CopyFeatures_management(veg_joined_table, outFeature)

def calculate_avg(ped_file_path, path_to_file):
    """
    this function calculate for each date avarage for each hour
    :param path_to_file: path to the result file in the specified date
    :return:
    """
    # for each date
    str_list = ped_file_path.split('_')
    new_date = str_list[-1] + '_' + str_list[-2]
    print(new_date)

    ped_file = pd.read_csv(path_to_file, index_col='via_to')
    ped_file.drop(columns='Unnamed: 0', inplace=True)

    #
    days["D_" +new_date] = ped_file.mean(axis=1)

# periods defination
inFeatures = os.path.join(os.path.split(os.getcwd())[0], 'links_network.shp')
data_source_folder = os.path.join(os.path.split(os.getcwd())[0], 'progress_files')
link_network = os.path.join(os.path.split(os.getcwd())[0], 'links_network.shp')
# period_dic = {'quarantine': {'files_2020': {'BTData_Mar2020': list(range(25, 31)),
#                                   'BTData_Apr2020': list(range(1, 8)) + list(range(11, 28))}}
# }
period_dic = {
    'before_corona': {'folder_2020': ['BTData_Feb2020'], 'files_2020': {'BTData_Mar2020': list(range(1, 8))}},
    'limited_gatherings_100': {'files_2020': {'BTData_Mar2020': list(range(11, 15))}},
    'limited_gatherings_10': {'files_2020': {'BTData_Mar2020': list(range(15, 25))}},
    'quarantine': {'files_2020': {'BTData_Mar2020': list(range(25, 31)),
                                  'BTData_Apr2020': list(range(1, 8)) + list(range(11, 28))}},
    'passover': {'files_2020': {'BTData_Apr2020': list(range(8, 12))}},
    'independence': {'files_2020': {'BTData_Apr2020': list(range(28, 30))}},
    'exit_quarantine': {'files_2020': {'BTData_Apr2020': list(range(30, 31)),
                                       'BTData_May2020': list(range(1, 27))}},
    'toward_2_wave': {'folder_2020': ['BTData_Jun2020', 'BTData_Jul2020'],
                      'files_2020': {'BTData_May2020': list(range(27, 32))}}}
for period in period_dic.keys():
    days = pd.DataFrame()
    if 'folder_2020' in period_dic[period]:
        work_with_folder('folder_2020')
    if 'files_2020' in period_dic[period]:
        work_with_files('files_2020')

    days.to_csv(os.path.join('maps',period + '.csv'))
for period in period_dic.keys():
    print('calculate join')
    join()
    print('finish join for {}'.format(period))