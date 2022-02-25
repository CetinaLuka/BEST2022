import os
import pandas as pd
import pyodbc

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
    unformatedData['Date'] = pd.to_datetime(unformatedData['Date'], format="%d/%m/%Y")
    unformatedData['Time'] = pd.to_datetime(unformatedData['Time'], format="%H:%M:%S").dt.time
    unformatedData.sort_values(by=["Date","Time"], inplace=True)
    return unformatedData

def importAccess():      
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:.\Baza.accdb;')
    cursor = conn.cursor()
    cursor.execute('select * from Data')
    data = cursor.fetchall()
    Data = pd.DataFrame(data)
    print(Data)

def manageData(data):
    averageByDate = data.groupby("Date").mean()
    averageByDate["Diff"] = averageByDate["Oil"].diff() * -1
    print(averageByDate.to_string())

#mergeFiles()
data = pd.read_csv("allData.csv")
data = formatData(data)

importAccess()
manageData(data)
