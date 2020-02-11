# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 10:27:51 2020
project name:2019-nCoV
Source From:CSDN
"""
import json, csv, requests  # 导入请求模块
import time
import os
import pickle
from opencage.geocoder import OpenCageGeocode
import xlwt
import xlrd
from xlutils.copy import copy

def add_line(work_sheet, row, count):
    for i in range(0, 6):
        work_sheet.write(count, i, row[i])

def get_data():  # 定义获取数据并写入csv文件里的函数
    url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"  # 请求网址
    response = requests.get(url).json()  # 发出请求并json化处理
    # print(response) #测试一下是否获取数据了
    data = json.loads(response['data'])  # 提取数据部分
    # print(data.keys()) #获取数据组成部分['chinaTotal', 'chinaAdd', 'lastUpdateTime', 'areaTree', 'chinaDayList', 'chinaDayAddList']
    update_time = data["lastUpdateTime"]

    recordDIR = "./data_record/"

    geokey = '0902cbf7651440a7b1b837648ac2eea2'  # get api key from:  https://opencagedata.com

    dayTime = update_time.split(" ", 2)[0]
    # timeStampNow = time.mktime(time.strptime(update_time, "%Y-%m-%d %H:%M:%S"))
    with open("day_update_record", "rb") as dayUpdateRecord:
        # 加载目前已经获取的天数的字典
        dayDict = pickle.load(dayUpdateRecord)
    with open("cityCord", "rb") as cordFile:
        cordDict = pickle.load(cordFile)

    dataAggDir = "./data_agg/"

    if dayTime not in dayDict.keys():
        # 获得新的一天的数据
        print("---------------------------")
        print("Add the data for a new day")
        areaTree = data["areaTree"]  # 各地方数据
        fileName = time.strftime("%Y-%m-%d-%H-%M", time.strptime(update_time, "%Y-%m-%d %H:%M:%S"))
        if len(os.listdir(dataAggDir)) == 0:
            work_book = xlwt.Workbook(encoding='gbk')
            sheet = work_book.add_sheet(fileName)
        else:
            rb = xlrd.open_workbook(dataAggDir + "data.xls")
            wb = copy(rb)
            sheet = wb.add_sheet(fileName)
        sheet.write(0, 0,"Province/State")
        sheet.write(0, 1, "Country/Region")
        sheet.write(0, 2, "Last Update")
        sheet.write(0, 3, "Confirmed")
        sheet.write(0, 4, "Recovered")
        sheet.write(0, 5, "Deaths")
        with open(recordDIR + fileName + "_data" + ".csv", "w+", newline="") as csv_file:
            writer = csv.writer(csv_file)
            header = ["Province/State","Country/Region","Last Update","Confirmed","Recovered","Deaths", "Date_last_updated","lat","lon"]
            Last_update =  time.strftime("%d/%m/%Y %H:%M", time.strptime(update_time, "%Y-%m-%d %H:%M:%S"))
            writer.writerow(header)
            china_data = areaTree[0]["children"]  # 中国数据
            geocoder = OpenCageGeocode(geokey)
            count = 0
            for j in range(len(china_data)):
                province = china_data[j]["name"]  # 省份
                city_list = china_data[j]["children"]  # 该省份下面城市列表
                for k in range(len(city_list)):
                    city_name = province + city_list[k]["name"]  # 城市名称
                    total_confirm = city_list[k]["total"]["confirm"]  # 总确认病例
                    # total_suspect = city_list[k]["total"]["suspect"]  # 总疑似病例
                    total_dead = city_list[k]["total"]["dead"]  # 总死亡病例
                    total_heal = city_list[k]["total"]["heal"]  # 总治愈病例
                    # today_confirm = city_list[k]["today"]["confirm"]  # 今日确认病例
                    # today_suspect = city_list[k]["total"]["suspect"]  # 今日疑似病例
                    # today_dead = city_list[k]["today"]["dead"]  # 今日死亡病例
                    # today_heal = city_list[k]["today"]["heal"]  # 今日治愈病例
                    # print(province, city_name, total_confirm, total_suspect, total_dead, total_heal, today_confirm,
                    #       today_suspect, today_dead, today_heal, update_time)
                    if city_name in cordDict.keys():
                        lat = cordDict[city_name][0]
                        lon = cordDict[city_name][1]
                    else:
                        query = city_list[k]["name"] + ',' + province + "," + "china"
                        results = geocoder.geocode(query)
                        lat = results[0]['geometry']['lat']
                        lon = results[0]['geometry']['lng']
                    data_row = [city_name, "China", Last_update, total_confirm, total_heal, total_dead,
                                update_time, lat, lon]
                    writer.writerow(data_row)
                    count += 1
                    add_line(sheet, data_row, count)

        dayDict[dayTime] = True
        with open("day_update_record", "wb") as dayUpdateRecord:
            pickle.dump(dayDict, dayUpdateRecord)

#     wb.save(dataDir + 'Excel表.xls')
        print("day {dayName} has been added".format(dayName=dayTime))
        print("---------------------------")

    else:
        # 一天中更新数据
        fileName = time.strftime("%Y-%m-%d-%H-%M", time.strptime(update_time, "%Y-%m-%d %H:%M:%S"))
        rb = xlrd.open_workbook(dataAggDir + "data.xls")
        wb = copy(rb)
        if fileName + "_data.csv" not in os.listdir("./data_record"):
            sheet = wb.add_sheet(time.strftime("%Y-%m-%d-%H-%M", time.strptime(update_time, "%Y-%m-%d %H:%M:%S")))
            sheet.write(0, 0, "Province/State")
            sheet.write(0, 1, "Country/Region")
            sheet.write(0, 2, "Last Update")
            sheet.write(0, 3, "Confirmed")
            sheet.write(0, 4, "Recovered")
            sheet.write(0, 5, "Deaths")
            print("---------------------------")
            print("update the data for day {dayname}".format(dayname=dayTime))
            areaTree = data["areaTree"]  # 各地方数据
            fileName = time.strftime("%Y-%m-%d-%H-%M", time.strptime(update_time, "%Y-%m-%d %H:%M:%S"))
            with open(recordDIR + fileName + "_data" + ".csv", "w+", newline="") as csv_file:
                writer = csv.writer(csv_file)
                header = ["Province/State", "Country/Region", "Last Update", "Confirmed", "Recovered", "Deaths",
                          "Date_last_updated", "lat", "lon"]
                Last_update = time.strftime("%d/%m/%Y %H:%M", time.strptime(update_time, "%Y-%m-%d %H:%M:%S"))
                writer.writerow(header)
                china_data = areaTree[0]["children"]  # 中国数据
                geocoder = OpenCageGeocode(geokey)
                count = 0
                for j in range(len(china_data)):
                    province = china_data[j]["name"]  # 省份
                    city_list = china_data[j]["children"]  # 该省份下面城市列表
                    for k in range(len(city_list)):
                        city_name = province + city_list[k]["name"]  # 城市名称
                        total_confirm = city_list[k]["total"]["confirm"]  # 总确认病例
                        total_dead = city_list[k]["total"]["dead"]  # 总死亡病例
                        total_heal = city_list[k]["total"]["heal"]  # 总治愈病例
                        if city_name in cordDict.keys():
                            lat = cordDict[city_name][0]
                            lon = cordDict[city_name][1]
                        else:
                            query = city_list[k]["name"] + ',' + province + "," + "china"
                            results = geocoder.geocode(query)
                            lat = results[0]['geometry']['lat']
                            lon = results[0]['geometry']['lng']
                        data_row = [city_name, "China", Last_update, total_confirm, total_heal, total_dead,
                                    update_time, lat, lon]
                        writer.writerow(data_row)
                        count += 1
                        add_line(sheet, data_row, count)

            print("day {dayName} has been updated at {uptime}".format(dayName=dayTime, uptime=update_time))
            print("---------------------------")
    if len(os.listdir(dataAggDir)) == 0:
        work_book.save(dataAggDir + "data.xls")
    else:
        os.remove(dataAggDir + "data.xls")
        wb.save(dataAggDir + "data.xls")


if __name__ == "__main__":
    while True:
        get_data()
        # 每各四个小时检查一遍更新
        time.sleep(14400)
