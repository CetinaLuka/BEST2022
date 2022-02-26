from io import StringIO
import os
from numpy import average
import pandas as pd
import pyodbc
from datetime import datetime, timedelta
import math

#db.importAccess() ---- KLIC CELOTNE TABELE IZ BAZE
#db.csvToAccess(calculatedData) --------- ZAPIS PODATKOV V BAZO
#db.importAccessDataForOneDay(calculatedData.at[0, "Date"].strftime("%Y-%m-%d")) --- KLIC POSAMEZNEGA ZAPISA


def importAccess():      
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=./Database/Baza.accdb;')
    data = pd.read_sql("SELECT mesure_date, mean, min, max, consumption, refil FROM Data", conn)
    Data = pd.DataFrame(data)
    Data.columns = ["Date", "Mean", "Min", "Max", "Diff", "Refil"]
    #print(Data)
    return Data.to_string()

def importAccessDataForOneDay(dateString):     
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=./Database/Baza.accdb;')
    data = pd.read_sql("SELECT mesure_date, mean, min, max, consumption, refil FROM Data WHERE mesure_date=#"+dateString+"#", conn)
    Data = pd.DataFrame(data)
    Data.columns = ["Date", "Mean", "Min", "Max", "Diff", "Refil"]
    #print(Data)
    return Data

def oneLineToAccess(data):
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=./Database/Baza.accdb;')
    cursor = conn.cursor()
    query = "SELECT count(Data.[id])FROM Data;"
    cursor.execute(query)
    num = cursor.fetchall()
    print("NUM: " + str(num[0][0]))
    for row in data.itertuples():
        print("ROW: " + str(row))
        cursor.execute('''
            INSERT INTO Data (id, mesure_date, mean, min, max, consumption, refil)
            VALUES (?,?,?,?,?,?,?)
            ''',
            num[0][0], 
            row.Date,
            row.Oil,
            row.Min,
            row.Max,
            row.Diff,
            "True " if row.Refil else "False"
            )
    conn.commit()

def oneLineAnomalyToAccess(data):
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=./Database/Baza.accdb;')
    cursor = conn.cursor()
    query = "SELECT count(Data.[id])FROM Anomalies;"
    cursor.execute(query)
    num = cursor.fetchall()
    print("NUM: " + str(num[0][0]))
    for row in data.itertuples():
        print("ROW: " + str(row))
        cursor.execute('''
            INSERT INTO Anomalies (id, mesure_date, mean, min, max, consumption, refil)
            VALUES (?,?,?,?,?,?,?)
            ''',
            num[0][0], 
            row.Date,
            row.Oil,
            row.Min,
            row.Max,
            row.Diff,
            "True " if row.Refil else "False"
            )
    conn.commit()

def csvToAccess(data):
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=./Database/Baza.accdb;')
    cursor = conn.cursor()
    for row in cursor.tables():
        if row.table_name == "Data":
            query = "DROP TABLE Data"
            cursor.execute(query)
            print (row.table_name)
            break
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
