from array import array
from datetime import datetime
from datetime import timedelta
from numpy import number
import pandas as pd
from datetime import date
import best2022 as best
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt

MIN_OIL = 1
#http://www.geostik.com/stat/ArhivPod.asp?Tip=K
TEMPERATURE_FILE = "temperaturaMaribor.csv"
COLUMN_TEMPERATURE = "Temperature"
COLUMN_DATE = "Date"
COLUMN_MONTH = "Month"
COLUMN_DAY = "Day"
COLUMN_AVERAGE7DAYS = "Average7Days"
TEMP_FORECAST = [11, 7.18, 4.55, 5.33, 5.84, 6.87, 8.76]
TEMP_FORECAST2 = [11, 7.18, 4.55, 5.33, 5.84, 6.87, 8.76,11, 7.18, 4.55, 5.33, 5.84, 6.87, 8.76,11, 7.18, 4.55, 5.33, 5.84, 6.87, 8.76,11, 7.18, 4.55, 5.33, 5.84, 6.87, 8.76,11, 7.18, 4.55, 5.33, 5.84, 6.87, 8.76,11, 7.18, 4.55, 5.33, 5.84, 6.87, 8.76,11, 7.18, 4.55, 5.33, 5.84, 6.87, 8.76,11, 7.18, 4.55, 5.33, 5.84, 6.87, 8.76,11, 7.18, 4.55, 5.33, 5.84, 6.87, 8.76,11, 7.18, 4.55, 5.33, 5.84, 6.87, 8.76,11, 7.18, 4.55, 5.33, 5.84, 6.87, 8.76,11, 7.18, 4.55, 5.33, 5.84, 6.87, 8.76,11, 7.18, 4.55, 5.33, 5.84, 6.87, 8.76,11, 7.18, 4.55, 5.33, 5.84, 6.87, 8.76,11, 7.18, 4.55, 5.33, 5.84, 6.87, 8.76,11, 7.18, 4.55, 5.33, 5.84, 6.87, 8.76,11, 7.18, 4.55, 5.33, 5.84, 6.87, 8.76,11, 7.18, 4.55, 5.33, 5.84, 6.87, 8.76,11, 7.18, 4.55, 5.33, 5.84, 6.87, 8.76,11, 7.18, 4.55, 5.33, 5.84, 6.87, 8.76,11, 7.18, 4.55, 5.33, 5.84, 6.87, 8.76]
AI_WEIGHT_TREND=0.5
AI_WEIGHT_FORMULA=0.5
DATA = best.manageData(best.formatData(pd.read_csv("allData.csv")))
    

def parseTemperature():
    data = pd.read_csv(TEMPERATURE_FILE, sep=";")
    data = formatTemperatureTable(data)
    return data


def formatTemperatureTable(unformatedData):
    unformatedData[COLUMN_DATE] = pd.to_datetime(
        unformatedData[COLUMN_DATE], format="%d. %m. %Y %H:%M:%S").dt.date
    unformatedData[COLUMN_TEMPERATURE].replace(
        ",", ".", inplace=True, regex=True)
    unformatedData.sort_values(by=[COLUMN_DATE], inplace=True)
    unformatedData[COLUMN_TEMPERATURE].str.strip()
    unformatedData = unformatedData.astype(
        {COLUMN_TEMPERATURE: "float64", COLUMN_DATE: "datetime64"})
    unformatedData = unformatedData.groupby(
        COLUMN_DATE)[COLUMN_TEMPERATURE].mean().reset_index()
    unformatedData[COLUMN_TEMPERATURE] = unformatedData[COLUMN_TEMPERATURE].round(
        1)
    unformatedData[COLUMN_MONTH] = unformatedData[COLUMN_DATE].dt.month
    unformatedData[COLUMN_AVERAGE7DAYS] = unformatedData[COLUMN_TEMPERATURE].rolling(
        2).mean()
    # unformatedData[COLUMN_DAY] = unformatedData[COLUMN_DATE].dt.dayofyear
    return unformatedData


# High quality AI
def calculateOilNeededBasedOnTheTemperature(temperature: number) -> float:
    return 0.135 - temperature/160

# Returns when we'll run out of oil. Returns "None" if we wont run out of fuel for all available forecasts. 
def getDateWhenWeWillRunOutOfOil(forecast: array, currentOil: number, currentDate = date.today()) -> datetime:
    totalConsumption = 0
    for i in range (len(forecast)):
        totalConsumption += getWeightedConsumption(currentDate, forecast[i], DATA, TREND)
        currentDate += timedelta(days=1)
        if(currentOil - totalConsumption < MIN_OIL):
            return currentDate
    return None

# Returns average consumption for next X days based on temperature. X is length of the array
def getEstimatedConsumptionForForecast(forecasts: array) -> float:
    total_consumption = 0
    currentDate = date.today()
    for forecast in forecasts:
        total_consumption += getWeightedConsumption(forecast)
        currentDate += timedelta(days=1)
    return total_consumption


def checkIfThereIsEnoughOil(fuelInTank: float, requiredForNext7Days: float, minGas = MIN_OIL) -> bool:
    if(fuelInTank > requiredForNext7Days + minGas):
        return True
    return False

def initTrendData() -> pd.DataFrame :
    data = pd.read_csv("allData.csv")
    data = best.formatData(data)
    managedData = best.manageData(data)
    parsedData = managedData[["Diff",COLUMN_DATE]]
    parsedData.loc[parsedData['Diff'] < 0, ['Diff']] = 0
    parsedData.dropna(subset = ["Diff"], inplace=True)
    parsedData = parsedData.set_index(COLUMN_DATE)
    decompose_result_mult = seasonal_decompose(parsedData, model="additive",extrapolate_trend='freq')
    return pd.DataFrame({"Date":decompose_result_mult.trend.index,"trend":decompose_result_mult.trend})

TREND = initTrendData()

def getWeightedConsumption(date:datetime, temperature: float, data:pd.DataFrame = DATA, trend:pd.DataFrame = TREND) -> float:
    data = data[data[COLUMN_DATE].isin(trend[COLUMN_DATE])]    
    data.loc[data['Diff'] < 0, ['Diff']] = 0

    oilNeededBasedOnTemp = calculateOilNeededBasedOnTheTemperature(temperature)
    oilConsumption = 0
    val = trend.loc[trend[COLUMN_DATE] == date]
    
    if(len(val) == 1):
        oilConsumption = oilNeededBasedOnTemp * AI_WEIGHT_FORMULA + val.iloc[0]["trend"] * AI_WEIGHT_TREND
    else:
        oilConsumption = oilNeededBasedOnTemp

    return (oilConsumption)



#------------------------------------------------------------------------------------------------------------------------------------------------------------
# #                      !Example of usage!  
#------------------------------------------------------------------------------------------------------------------------------------------------------------

# data = pd.read_csv("allData.csv")
# data = best.formatData(data)
# managedData = best.manageData(data)

# temperature = parseTemperature()
# managedData = pd.concat([managedData.set_index(COLUMN_DATE),temperature.set_index(COLUMN_DATE)], axis=1, join='inner').reset_index()

# arraya = []
# for i, row in managedData.iterrows():
#     arraya.append(getWeightedConsumption(row["Date"],row["Temperature"]))

# print(arraya)
# print(managedData)
# managedData.loc[managedData['Diff'] < 0, ['Diff']] = 0
# managedData.loc[managedData['Diff'] > 0.3, ['Diff']] = 0.1
# print(consumption)
# print(data)
# runOut = getDateWhenWeWillRunOutOfOil(TEMP_FORECAST2,1.2)
# print(runOut)
#------------------------------------------------------------------------------------------------------------------------------------------------------------


# AI part, which didn't really work..

# data2 = parseTemperature()
# x = data2[COLUMN_DATE]

# # # print(trend.to_string())
# # # decompose_result_mult.plot()
# # # plt.show()


# y2 = managedData[managedData[COLUMN_DATE].isin(x)]

# y = data2[data2[COLUMN_DATE].isin(y2[COLUMN_DATE])]
# y["Temperature"] = calculateFuelNeededBasedOnTheTemperature(y["Temperature"])


# y2 = y2[y2['Diff'] > -0.5]
# y2["Povp"] = y2["Diff"].rolling(1).mean()
# sns.lineplot( x = 'Date',
#              y = COLUMN_TEMPERATURE,
#              data = y,
#              label = 'Temperature')
# sns.lineplot( x = 'Date',
#              y = "Povp",
#              data = y2,
#              label = 'Consumption')
# plt.show()


# # # # # # X_train, X_test, y_train, y_test = train_test_split(y, y2, test_size=0.2, random_state=42)

# # # # # # mlTrain = X_train.drop("Date", axis=1)
# # # # # # mlYTrain = y_train["Diff"] * 10000
# # # # # # mlYTrain = mlYTrain.astype(int)

# # # # # # print(mlTrain)
# # # # # # print("---------------------------")

# # # # # # clf = MLPClassifier(hidden_layer_sizes=(6,5),
# # # # # #                     random_state=5,
# # # # # #                     verbose=True,
# # # # # #                     learning_rate_init=0.1)
# # # # # # clf.fit(mlTrain,mlYTrain)
# # # # # # mlTest = X_test.drop("Date", axis=1)
# # # # # # ypred=clf.predict(mlTest)

# # # # # # # Calcuate accuracy
# # # # # # # print(y_test["Diff"],ypred/1000000)

# # # # # # y_test["pred"] = ypred/10000
# # # # # # y_test["error"] = y_test["Diff"] - y_test["pred"]
# # # # # # y_test = y_test[y_test["Refil"] == False]
# # # # # # print(y_test)
# # # # # # print(y_test["error"].mean())
# plt.plot(managedData[COLUMN_DATE],arraya, label="Predicted")
# plt.plot(managedData[COLUMN_DATE],managedData["Diff"], label="Consumption")
# plt.legend(loc="upper right")
# # plt.ylim(-1.5, 2.0)
# plt.show()
