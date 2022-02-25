import pandas as pd
import best2022 as best

MAX_CONSUMPTION = 0.4

def checkIfConsumptionIsWithinRange(row:pd.DataFrame):
        if(row["Diff"] > MAX_CONSUMPTION):
            #TODO pošlji email obvestilo da je poraba presegla threshold
            print("Pošlji mail, kjer je poraba več kot MAX_CONSUMPTION poraba je:", row["Diff"])


data = pd.read_csv("allData.csv")
data = best.formatData(data)
managedData = best.manageData(data)
for index, row in managedData.iterrows():
    checkIfConsumptionIsWithinRange(row)
    