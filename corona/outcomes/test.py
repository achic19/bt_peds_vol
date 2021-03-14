import pandas as pd
import os
file_1 = r'D:\Users\OneDrive - Technion\PhD\research\big_data_padestrian_flow\bt_peds_vol\corona\progress_files\BTData_May2020\file2020_05_21\results.csv'
file_2 = r'D:\Users\OneDrive - Technion\PhD\research\big_data_padestrian_flow\bt_peds_vol\corona\progress_files\BTData_May2020\file2020_05_24\results.csv'
ped_file_high = pd.read_csv(file_1, index_col='via_to')
ped_file_low = pd.read_csv(file_2, index_col='via_to')
links_list = list(pd.read_csv('links_file.csv')['link_names'])
ped_file_low.drop(columns='Unnamed: 0',inplace=True)
ped_file_high.drop(columns='Unnamed: 0',inplace=True)
ped_file_low = ped_file_low.loc[:,list(map(str, range(6, 24)))]
ped_file_low = ped_file_low[ped_file_low.index.isin(links_list)]
print(ped_file_low.mean().mean())

ped_file_high = ped_file_high.loc[:,list(map(str, range(6, 24)))]
ped_file_high = ped_file_high[ped_file_high.index.isin(links_list)]
print(ped_file_high.mean().mean())

subtract_weekdays = ped_file_low.subtract(ped_file_high, axis=1).dropna()
avg =subtract_weekdays.mean()
print(avg.mean())
print(avg)
# num_list = [1, 2, 3, 4, 5]
# # num_list[2:].append(7)
# print((num_list[2:]).append(7))

# print(list(range(3)) + list(range(2)))
# Name: AttributeSelection.py
# Purpose: Join a table to a featureclass and select the desired attributes

# Import system modules
# import arcpy
# import os
# # Set environment settings
# arcpy.env.workspace = os.getcwd()
# arcpy.env.qualifiedFieldNames = False
#
#
# if os.path.exists('vegjoin.shp'):
#     for item in ['shp','shx','cpg','dbf','prj']:
#         os.remove('vegjoin.' + item)
#
# # # Execute TableToTable
# # inTable = "passover.csv"
# # outLocation = os.getcwd()
# # outTable = "passover.dbf"
# # arcpy.TableToTable_conversion(inTable, outLocation, outTable)
#
# # Set local variables
# inFeatures = os.path.join(os.path.split(os.getcwd())[0], 'links_network.shp')
# joinTable = "passover.csv"
# joinField = "via_to"
# outFeature = "vegjoin.shp"

# # Join the feature layer to a table
# veg_joined_table = arcpy.AddJoin_management(inFeatures, joinField, joinTable,joinField)
#
#
# # Copy the layer to a new permanent feature class
# arcpy.CopyFeatures_management(veg_joined_table, outFeature)
# idx = pd.Index(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
#                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
# if not 'Aug' in idx:
#     print('good')
# t= False
# if not t:
#     print('good')
# range_1 = list(range(0, 11))
# range_2 = list(range(-5, 0))
# print(range_1+range_2)
# weekdays = pd.DataFrame(columns=list(map(str, range(0, 24))))
# ped = pd.read_csv('test.csv', index_col='via_to')
# ped.drop(columns='Unnamed: 0', inplace=True)
#
# weekdays.loc['26.2']= ped.loc['TA104TA257']
# ped = pd.read_csv('test2.csv', index_col='via_to')
# ped.drop(columns='Unnamed: 0', inplace=True)
#
# weekdays.loc['25.2'] =ped.loc['TA111TA134']
# print(weekdays)
# df = pd.DataFrame(data= g.values(),index=list(g.keys()),columns=['ped_count1'])
# df2 = pd.DataFrame(data= g2.values(),index=list(g2.keys()),columns=['ped_count1'])
# df3 = df2.subtract(df, axis = 1).dropna().abs().sort_values(by ='ped_count1',ascending=False).reset_index()
# print(df3)
# for i in range(-3,0):
#     print(df3.iloc[i]['index'])

# tst= '02'
# print(len(tst))
# weekends = pd.DataFrame(index=list(map(str,range(0, 24))))
# dt = pd.DataFrame([20,60,70], index=['1','2','3'])
# weekends['hdsklf'] =dt
# print(weekends)
# print(weekends.mean(axis=0))

#
# g = {"a":[1], "b":[5]}
# df = pd.DataFrame(data= g.values(),index=list(g.keys()),columns=['ped_count'])
# print(df)

# g = list(range(0,24))
# g =list(map(str,g))
# print(g)