from io import StringIO
import os
from numpy import average
import pandas as pd
import pyodbc
from datetime import datetime, timedelta
import math
import Modules.dataBase_util as db

def mergeFiles():
    print("Merge all files")
    mainFileName = "allData.csv"
    if os.path.exists(mainFileName):
        os.remove(mainFileName)
    allData = open(mainFileName, "a+")
    allData.write("Date,Time,Oil\n")
    path = 'Arhiv_2021'
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

def readNewFile():
    yesterday = datetime.today() - timedelta(days=1)
    before_yesterday = datetime.today() - timedelta(days=2)
    before_yesterday = before_yesterday.replace(year=2021)
    d = yesterday.strftime("%d_%m_%Y")
    print(d)
    print(before_yesterday.strftime("%Y-%m-%d"))
    #csvFile = "./Data/"+d+".csv"
    #data = open(csvFile, "w+")
    #data.write("Date,Time,Oil\n")
    currFile = open("./Data/"+d+".TXT", "r")
    lines = currFile.readlines()
    csvString = "Date,Time,Oil\n"
    for line in lines:
        line = line.replace(" ", "")
        line = line[0:10] + "," + line [10:]
        line = line.replace("!", ",")
        csvString = csvString + line+"\n"
        #data.write(line)
    currFile.close()
    df = pd.read_csv(StringIO(csvString), sep=",")
    df = formatData(df)
    accessData = db.importAccessDataForOneDay(str(before_yesterday.strftime("%Y-%m-%d")))
    print(accessData)
    joinedData = pd.concat([accessData, df])
    print(joinedData)
    managedData = manageData(joinedData)
    print(managedData)
    return str(csvString)

def formatData(unformatedData):
    unformatedData['Date'] = pd.to_datetime(unformatedData['Date'], format="%d/%m/%Y")
    unformatedData['Time'] = pd.to_datetime(unformatedData['Time'], format="%H:%M:%S").dt.time
    unformatedData.sort_values(by=["Date","Time"], inplace=True)
    return unformatedData

def manageData(data):
    dataByDate = data.groupby("Date")["Oil"].mean().reset_index()
    minByDate = data.groupby("Date")["Oil"].min().reset_index()
    maxByDate = data.groupby("Date")["Oil"].max().reset_index()
    dataByDate ["Min"] = minByDate["Oil"]
    dataByDate ["Max"] = maxByDate["Oil"]
    dataByDate["Diff"] = dataByDate["Oil"].diff() * -1
    dataByDate.at[0, "Diff"] = 0
    dataByDate["Refil"] = dataByDate["Max"] - dataByDate["Min"] > 1
    return dataByDate

#mergeFiles()
#data = pd.read_csv("../../allData.csv")
#data = formatData(data)

#importAccess()
#data = manageData(data)
#csvToAccess(data)