from io import StringIO
import os
from numpy import average
import pandas as pd
import pyodbc
from datetime import datetime, timedelta
import math

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
    before_yesterday = before_yesterday.strftime("%#d/%m/")+"2021"
    d = yesterday.strftime("%d_%m_%Y")
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
    oil_before_yesterday = importOilDataForOneDay(before_yesterday)
    calculated_data = calculate_consumption(df, oil_before_yesterday)
    return calculated_data.iloc[0]

def formatData(unformatedData):
    unformatedData['Date'] = pd.to_datetime(unformatedData['Date'], format="%d/%m/%Y")
    unformatedData['Time'] = pd.to_datetime(unformatedData['Time'], format="%H:%M:%S").dt.time
    unformatedData.sort_values(by=["Date","Time"], inplace=True)
    return unformatedData

def importAccess():      
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=./Database/Baza.accdb;')
    cursor = conn.cursor()
    cursor.execute('select * from Data')
    data = cursor.fetchall()
    Data = pd.DataFrame(data)
    print(Data)
    return Data.to_string()

def importOilDataForOneDay(dateString):      
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=./Database/Baza.accdb;')
    cursor = conn.cursor()
    query = 'select Oil from Data where Date=#'+dateString+'#'
    #db_data = pd.read_sql(query, conn)
    #print(db_data)
    cursor.execute(query)
    data = cursor.fetchall()
    #Data = pd.DataFrame(data)
    return data

def csvToAccess(data):
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=../Database/Baza.accdb;')
    cursor = conn.cursor()
    query = "DROP TABLE Data"
    cursor.execute(query)
    cursor.execute('''
		CREATE TABLE Data (
			id INT primary key,
			mesure_date DATE,
			mean DOUBLE,
			min DOUBLE,
			max DOUBLE,
			consumption DOUBLE,
			refil varchar(10)
			)
              ''')
    for row in data.itertuples():
        cursor.execute('''
            INSERT INTO Data (id, mesure_date, mean, min, max, consumption, refil)
            VALUES (?,?,?,?,?,?,?)
            ''',
            row.Index, 
            row.Date,
            row.Oil,
            row.Min,
            row.Max,
            row.Diff,
            "True " if row.Refil else "False"
            )

    conn.commit()

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

def calculate_consumption(data, yesterdays_oil_value):
    data.iloc[-1, data.columns.get_loc('Date')] = data.iloc[-2, data.columns.get_loc('Date')]
    dataByDate = data.groupby("Date")["Oil"].mean().reset_index()
    minByDate = data.groupby("Date")["Oil"].min().reset_index()
    maxByDate = data.groupby("Date")["Oil"].max().reset_index()
    dataByDate ["Min"] = minByDate["Oil"]
    dataByDate ["Max"] = maxByDate["Oil"]
    dataByDate["Diff"] = yesterdays_oil_value - dataByDate.iloc[0]["Oil"]
    dataByDate["Refil"] = dataByDate["Max"] - dataByDate["Min"] > 1
    return dataByDate

#mergeFiles()
#data = pd.read_csv("../../allData.csv")
#data = formatData(data)

#importAccess()
#data = manageData(data)
#csvToAccess(data)