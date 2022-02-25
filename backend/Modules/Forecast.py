from numpy import float64
import best2022 as best
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score


MIN_GAS = 1
#http://www.geostik.com/stat/ArhivPod.asp?Tip=K
TEMPERATURE_FILE="temperaturaMaribor.csv"
COLUMN_TEMPERATURE="Temperature"
COLUMN_DATE="Date"

def parseTemperature():
    data = pd.read_csv(TEMPERATURE_FILE, sep=";")
    data = formatTemperatureTable(data)
    return data
    
def formatTemperatureTable(unformatedData):
    unformatedData[COLUMN_DATE] = pd.to_datetime(unformatedData[COLUMN_DATE], format="%d. %m. %Y %H:%M:%S").dt.date
    unformatedData[COLUMN_TEMPERATURE].replace(",",".", inplace=True, regex=True)
    unformatedData.sort_values(by=[COLUMN_DATE], inplace=True)
    unformatedData[COLUMN_TEMPERATURE].str.strip()
    unformatedData = unformatedData.astype({COLUMN_TEMPERATURE: "float64", COLUMN_DATE: "datetime64"})
    unformatedData = unformatedData.groupby(COLUMN_DATE)[COLUMN_TEMPERATURE].mean().reset_index()
    unformatedData[COLUMN_TEMPERATURE] = unformatedData[COLUMN_TEMPERATURE].round(1)
    return unformatedData


def getEstimatedDaysUntilRefuelNeeded():
    print("asd")
    
data2 = parseTemperature()
x = data2[COLUMN_DATE]


data = pd.read_csv("allData.csv")
data = best.formatData(data)
managedData = best.manageData(data)

y2 = managedData[managedData[COLUMN_DATE].isin(x)]
# y2["Diff"] *= 140
# y2["Diff"] = 20 - y2["Diff"] 
# y2 = y2[y2['Diff'] > -10]
# y2 = y2[y2['Diff'] < 40]

y = data2[data2[COLUMN_DATE].isin(y2[COLUMN_DATE])]
# y["Diff"] = y[COLUMN_TEMPERATURE].diff()


X_train, X_test, y_train, y_test = train_test_split(y, y2, test_size=0.2, random_state=42)

mlTrain = X_train[COLUMN_TEMPERATURE].values.reshape(-1,1)
mlYTrain = y_train["Diff"] * 10000000000
mlYTrain = mlYTrain.astype(int)
clf = MLPClassifier(hidden_layer_sizes=(6,5),
                    random_state=5,
                    verbose=True,
                    learning_rate_init=0.01)
clf.fit(mlTrain,mlYTrain)
ypred=clf.predict(X_test[COLUMN_TEMPERATURE].values.reshape(-1,1))

# Calcuate accuracy
# print(y_test["Diff"],ypred/1000000)

y_test["pred"] = ypred/10000000000
y_test["error"] = y_test["Diff"] - y_test["pred"]
y_test = y_test[y_test["Refil"] == False]
print(y_test)
print(y_test["error"].mean())

# plt.plot(y2[COLUMN_DATE],y[COLUMN_TEMPERATURE])
# plt.plot(y2[COLUMN_DATE],y2["Diff"])
y_test = y_test.sort_values(by="Date")
plt.plot(y_test[COLUMN_DATE],y_test["pred"])
plt.plot(y_test[COLUMN_DATE],y_test["Diff"])
plt.show()