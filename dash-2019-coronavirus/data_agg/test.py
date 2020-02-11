# from opencage.geocoder import OpenCageGeocode
# from datetime import datetime
# # import time
# key = '0902cbf7651440a7b1b837648ac2eea2'  # get api key from:  https://opencagedata.com
# geocoder = OpenCageGeocode(key)
#
# City = "Taiwan"
# State = "China"
# query = str(City)+','+str(State)
#
# results = geocoder.geocode(query)
# lat = results[0]['geometry']['lat']
# long = results[0]['geometry']['lng']
#
# print(lat)
# print(long)

# nowtime = "2020-02-10 15:36:16"
# dayTime = nowtime.split(" ", 2)[0]
# print(dayTime)
# print(time.mktime(time.strptime(nowtime, "%Y-%m-%d %H:%M:%S")))
#
# import pickle
# #
# dict = {}
# with open("day_update_record", "wb") as obj:
#     pickle.dump(dict, obj)
# import xlwt
# import xlrd
# from xlutils.copy import copy
# import os
# dataDir = "./data_agg/"
# nowtime = "2020-02-10-15-36"
# nexttime = "2020-02-10-15-37"
# if len(os.listdir(dataDir)) == 0:
#     work_book = xlwt.Workbook(encoding='gbk')
#     sheet = work_book.add_sheet(nowtime)
#     sheet.write(0, 0, 2292292)
#     sheet.write(0, 1, '第一行第二列')
#     work_book.save(dataDir + 'Excel表.xls')
# else:
#     rb = xlrd.open_workbook(dataDir + 'Excel表.xls')
#     wb = copy(rb)
#     sheet = wb.add_sheet(nexttime)
#     sheet.write(0,0,22222)
#     os.remove(dataDir + 'Excel表.xls')
#     wb.save(dataDir + 'Excel表.xls')
# styleBoldRed = xlwt.easyxf('font: color-index red, bold on')
#
# headerStyle = styleBoldRed
#
# wb = xlwt.Workbook()
#
# ws = wb.add_sheet("")
#
# ws.write(0, 0, "Header", headerStyle)
#
# ws.write(0, 1, "CatalogNumber", headerStyle)
#
# ws.write(0, 2, "PartNumber", headerStyle)
#
# wb.save(gConst['xls']['fileName'])
#
#
#
# oldWb = xlrd.open_workbook(gConst['xls']['fileName'], formatting_info=True)
#
#
# newWb = copy(oldWb)
#
# print
# newWb;  # <xlwt.Workbook.Workbook object at 0x000000000315F470>
#
# newWs =
# newWb.get_sheet(0);
#
# newWs.write(1, 0, "value1")
#
# newWs.write(1, 1, "value2")
#
# newWs.write(1, 2, "value3")
#
# newWb.save(gConst['xls']['fileName'])

import pandas as pd
import pickle
cordDict = {}
currFile = pd.read_csv('./data_record/2020-02-10-23-05_data.csv', encoding="gbk")

# cityName = currFile["Province/State"]
# latList = currFile["lat"]
# lonList = currFile["lon"]
# for i in range(len(cityName)):
#     if "澳门" in cityName[i]:
#         cord = (22.1757605,113.5514142)
#         cordDict[cityName[i]] = cord
#         continue
#     if "台湾" in cityName[i]:
#         cord = (23.9739374,120.9820179)
#         cordDict[cityName[i]] = cord
#         continue
#     cord = (latList[i], lonList[i])
#     cordDict[cityName[i]] = cord
# print(cordDict)
# with open("cityCord", "wb") as obj:
#     pickle.dump(cordDict, obj)

