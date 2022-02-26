import pandas as pd
import best2022 as best
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
from sklearn.covariance import EllipticEnvelope
from sklearn.neighbors import KernelDensity

REFILL_DIFF_VAL = 0.3
CALCULATE_RANGE = 20

def getListOfRefils(calculatedData):
    refils = calculatedData.loc[calculatedData["Refil"]]
    return refils

def manageRawData(calculatedData, rawData):
    refils = getListOfRefils(calculatedData)
    for i in range(len(refils)):
        dataIndex = refils.index[i]
        ref = rawData.loc[rawData["Date"] == (refils.iloc[i]["Date"])]
        ref = ref.reset_index()
        ref["Diff"] = ref["Oil"].diff()
        ref["Refil"] = abs(ref["Diff"]) > REFILL_DIFF_VAL #TODO: UI HERE ;)
        #print(ref.to_string())
        beforeIndex = ref[ref.Refil].head(1).index[0]
        afterIndex = ref[ref.Refil].tail(1).index[0]
        before = ref[:beforeIndex]
        after = ref[afterIndex:]
        before_start = before.head(CALCULATE_RANGE)["Oil"].mean()
        before_end = before.tail(CALCULATE_RANGE)["Oil"].mean()
        #print("Before_S:" + str(before_start))
        #print("Before_E:" + str(before_end))
        after_start = after.head(CALCULATE_RANGE)["Oil"].mean()
        after_end = after.tail(CALCULATE_RANGE)["Oil"].mean()
        #print("After_S:" + str(after_start))
        #print("After_E:" + str(after_end))
        oilRefil = after_start - before_end
        #print(dataIndex)
        #print("Refil: " + str(oilRefil))
        dailyDiff = (before_start - before_end) + (after_start - after_end)
        #print("Daily diff: " + str(dailyDiff)) 
        calculatedData.at[dataIndex, "Diff"] = dailyDiff
        nextDay = after_end - calculatedData.at[dataIndex+1, "Oil"]
        calculatedData.at[dataIndex+1, "Diff"] = nextDay
        #TODO:POŠLJI EMAIL - DOLIVANJE OLJA
    #print(calculatedData.to_string())
    
def findAnomalies(data):
    model=IsolationForest(n_estimators=50, max_samples='auto', contamination=float(0.1),max_features=1.0)
    model.fit(data[['Oil']])

    #data['scores']=model.decision_function(data[['Oil']])
    data['anomalyIF']=model.predict(data[['Oil']])
    
    #anomaly=data.loc[data['anomalyIF']==-1]
    #anomaly_index=list(anomaly.index)
    #print(len(data.index))
    #print(len(anomaly.index))

    model=OneClassSVM(kernel='rbf', gamma=0.001, nu=0.2)
    model.fit(data[['Oil']])

    data['anomalySVM']=model.predict(data[['Oil']])
    
    #anomaly=data.loc[data['anomalySVM']==-1]
    #print(len(anomaly.index))

    model=LocalOutlierFactor(n_neighbors=40, novelty=True, contamination=0.4)
    model.fit(data[['Oil']])

    data['anomalyLOF']=model.predict(data[['Oil']])
    
    #anomaly=data.loc[data['anomalyLOF']==-1]
    #print(len(anomaly.index))

    model= EllipticEnvelope(contamination=.2)
    model.fit(data[['Oil']])

    data['anomalyEE']=model.predict(data[['Oil']])
    
    #anomaly=data.loc[data['anomalyEE']==-1]
    #print(len(anomaly.index))

    model=KernelDensity(bandwidth = 0.2, kernel='gaussian')#tophat
    model.fit(data[['Oil']])

    data['anomalyKD']=model.score_samples(data[['Oil']])
    
    #anomaly=data.loc[data['anomalyKD']<-3]
    #print(len(anomaly.index))

    #with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #    print(data)
    
    anomalies=pd.DataFrame(data.loc[(data['anomalyIF']==-1)&(data['anomalySVM']==-1)&(data['anomalyLOF']==-1)&(data['anomalyEE']==-1)&(data['anomalyKD']<-3)])
    return anomalies

rawData = pd.read_csv("../../allData.csv")
formatedData = best.formatData(rawData)
calculatedData = best.manageData(formatedData)
print(calculatedData)
manageRawData(calculatedData, rawData)

print(findAnomalies(calculatedData))
    