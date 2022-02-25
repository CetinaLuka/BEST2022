import pandas as pd
import Modules.best2022 as best

def getmanagedData():
    data = pd.read_csv("./Data/allData.csv")
    data = best.formatData(data)
    managedData = best.manageData(data)
    #print(managedData)
    return managedData;