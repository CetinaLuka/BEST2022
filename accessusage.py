import pyodbc
import pandas as pd

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:.\Baza.accdb;')
cursor = conn.cursor()
cursor.execute('select * from Data')
   
#for row in cursor.fetchall():
    #print (row)

#sql = "select * from Data"
#data = pd.read_sql(sql,conn)

data = cursor.fetchall()
Data = pd.DataFrame(data)
print(Data)