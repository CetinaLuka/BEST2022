from io import StringIO
import os
from numpy import average
import pandas as pd
import pyodbc
import Modules.DetectRefills as detect_refills
from datetime import datetime, timedelta, time
import math
import Modules.dataBase_util as db

def mergeFiles():
    print("Merge all files")
    mainFileName = "../allData.csv"
    if os.path.exists(mainFileName):
        os.remove(mainFileName)
    allData = open(mainFileName, "a+")
    allData.write("Date,Time,Oil\n")
    path = '../Arhiv_2021/osnova/'
    arr = os.listdir(path)
    for folder in arr:
        arrFile = os.listdir(path + "/" + folder)
        fileName = arrFile[0]
        currFile = open(path + "/" + folder + "/" + fileName, "r")
        lines = currFile.readlines()
        for line in lines:
            line = line.replace(" ", "")
            line = line[0:10] + "," + line [10:]
            line = line.replace("!", ",")
            allData.write(line)
        currFile.close()

def readNewFile(currentDate):
    yesterday = currentDate - timedelta(days=1)
    #before_yesterday = currentDate - timedelta(days=2)
    #print(currentDate)
    #print (yesterday)
    file = str(currentDate.strftime("../Arhiv_2021/napoved/Arhiv_%d_%m_%Y"))
    arr = os.listdir(file)
    currCsv = open("../currData.csv", "w")
    currCsv.write("Date,Time,Oil\n")
    currFile = open(file+"/"+arr[0])
    lines = currFile.readlines()
    for line in lines:
        line = line.replace(" ", "")
        line = line[0:10] + "," + line [10:]
        line = line.replace("!", ",")
        currCsv.write(line)
    currCsv.close()
    currData = pd.read_csv("../currData.csv")
    rawData = formatData(currData)
    rawData.at[len(rawData)-1, "Date"] = rawData.at[len(rawData)-1, "Date"] - timedelta(days=1)
    rawData.at[len(rawData)-1, "Time"] = time(hour=23, minute=59, second=59)
    yesterdayData = db.importAccessDataForOneDay(yesterday.strftime("%Y-%m-%d"))
    isYesterdayRefil = yesterdayData.Refil == "True"
    print(isYesterdayRefil)
    #print(yesterdayData)
    #print(rawData)
    data = manageData(rawData)
    #print(yesterdayData.Mean)
    data.at[0, "Diff"] = yesterdayData.Mean - data.at[0, "Oil"]
    #print(data)
    return rawData, data, isYesterdayRefil

def formatData(unformatedData):
    unformatedData['Date'] = pd.to_datetime(unformatedData['Date'], format="%d/%m/%Y")
    unformatedData['Time'] = pd.to_datetime(unformatedData['Time'], format="%H:%M:%S").dt.time
    unformatedData.sort_values(by=["Date","Time"], inplace=True)
    #print(unformatedData)
    return unformatedData

def manageData(data):
    data = data[:-1]
    dataByDate = data.groupby("Date")["Oil"].mean().reset_index()
    minByDate = data.groupby("Date")["Oil"].min().reset_index()
    maxByDate = data.groupby("Date")["Oil"].max().reset_index()
    dataByDate ["Min"] = minByDate["Oil"]
    dataByDate ["Max"] = maxByDate["Oil"]
    dataByDate["Diff"] = dataByDate["Oil"].diff() * -1
    dataByDate.at[0, "Diff"] = 0
    dataByDate["Refil"] = dataByDate["Max"] - dataByDate["Min"] > 1
    return dataByDate

def readPrevData():
    mergeFiles()
    data = pd.read_csv("../allData.csv")
    rawData = formatData(data)
    data = manageData(rawData)
    return rawData, data

#mergeFiles()
#
#data = formatData(data)

#importAccess()
#data = manageData(data)
#csvToAccess(data)