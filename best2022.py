from email.utils import formatdate
import os
import pandas as pd

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

def formatData(unformatedData):
    unformatedData['Date'] = pd.to_datetime(data['Date'], format="%d/%m/%Y")
    unformatedData['Time'] = pd.to_datetime(data['Time'], format="%H:%M:%S").dt.time
    unformatedData.sort_values(by=["Date","Time"], inplace=True)
    return unformatedData

#mergeFiles()
data = pd.read_csv("allData.csv")
data = formatData(data)

print(data.to_string())
