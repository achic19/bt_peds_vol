import os

import geopandas as gpd
import pandas as pd


# def get_list_of_links_names(links: pd.DataFrame, via, to):
#     """
#     :param to: column in the dataframe helping to make it one direction
#     :param via: column in the dataframe helping to make it one direction
#     :param links: to make it one directional and as list of link names
#     :return: list of link names
#     """
#     # Make it one directional by change the “via_to” field (if necessary) to smaller first
#     links['via_to'] = links.apply(lambda row: list_to_str(row), axis=1)
#     for index, row in links.iterrows():
#         if row[via] > row[to]:
#             all_links.at[index, 'via_to'] = row[to] + row[via]
#     return list(all_links.groupby('via_to').groups.keys())


def to_one_direction(row):
    if row['VIAUNITC'] > row['TOUNITC']:
        return row['TOUNITC'] + row['VIAUNITC']
    else:
        return row['VIAUNITC'] + row['TOUNITC']


if __name__ == '__main__':
    # parameters for developing phase , file parameter relate to the file to start run from
    # (for specific folder in floder parameter) summery paraemter means create new one based on or use one
    # in the disk , source parameter relate to the csv file source ( file from tsmart with no date column)
    parameters = {'folder': 'BTData_Ocb2019', 'file': 2, 'summery': True, 'source':'tsmart'}
    # read all links file ,Make it one directional ,and get their names
    all_links = gpd.read_file('GIS project1/shpfile/all_links.shp')
    # Make it one directional by change the “via_to” field (if necessary) to smaller first
    for index, row in all_links.iterrows():
        if row['VIA'] > row['TO']:
            all_links.at[index, 'via_to'] = row['TO'] + row['VIA']
    all_links_names = list(all_links.groupby('via_to').groups.keys())
    # new dataframe with links as indexes
    if parameters['summery']:
        summery = pd.read_csv('summery.csv', index_col=0)
    else:
        summery = pd.DataFrame(index=all_links_names)

    # folder to get files from order by dates
    # month_list = ['BTData_Jul2019', 'BTData_Ocb2019', 'BTData_Nov2019_Updated',
    #               'BTData_Dec2019_Updated', 'BTData_jan2020', 'BTData_Feb2020', 'BTData_Mar2020', 'BTData_Apr2020'
    #                                                                                               'BTData_May2020',
    #               'BTData__June2020_to_23']
    month_list = [ 'August_working_links']
    for folder in month_list:
        print(folder)
        for i, file_name in enumerate(os.listdir(folder)):
            if folder == parameters['folder']:
                if i < parameters['file']:
                    continue
            print("  " + file_name)
            curr_file = pd.read_csv(os.path.join(folder, file_name))
            # delete rows with null vualues in 'VIAUNITC' or 'TOUNITC'
            curr_file = curr_file[pd.notna(curr_file['VIAUNITC'])]
            curr_file = curr_file[pd.notna(curr_file['TOUNITC'])]
            # to one direction link
            curr_file['via_to'] = curr_file.apply(lambda row: to_one_direction(row), axis=1)
            # curr_file.to_csv('test.csv')
            # group by link name
            links_names = list(curr_file.groupby('via_to').groups.keys())
            # save only links exist in all_links_names
            links_in_all_links = list(set(links_names) & set(all_links_names))
            # update the summery dataframe with new column and data ( if the file is created by tsmart take the date from the file name
            if parameters['source'] =='tsmart':
                new_column = file_name.split('.')[0].split('e')[1]
            else:
                new_column = str(curr_file['date'].iloc[0])
            summery[new_column] = 0
            summery.loc[links_in_all_links, new_column] = 1
            summery.to_csv('summery.csv')

    # calculate sum to each row
    summery['sum'] = summery.sum(axis=1)
    summery.to_csv('summery.csv')
