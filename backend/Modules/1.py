import pandas as pd
import best2022 as best
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
    calculatedData.to_csv("../../editedData.csv")
    
def findAnomalies(data):
    model=IsolationForest(n_estimators=50, max_samples='auto', contamination=float(0.1),max_features=1.0)
    model.fit(data[['Oil']])

    data['scores']=model.decision_function(data[['Oil']])
    data['anomaly']=model.predict(data[['Oil']])
    
    anomaly=data.loc[data['anomaly']==-1]
    anomaly_index=list(anomaly.index)
    print(len(data.index))
    print(len(anomaly.index))

    model=OneClassSVM(kernel='rbf', gamma=0.001, nu=0.03)
    model.fit(data[['Oil']])

    data['scores']=model.decision_function(data[['Oil']])
    data['anomaly']=model.predict(data[['Oil']])
    
    anomaly=data.loc[data['anomaly']==-1]
    anomaly_index=list(anomaly.index)
    print(len(data.index))
    print(len(anomaly.index))

    model=LocalOutlierFactor(n_neighbors=20, novelty=True, contamination=0.1)
    model.fit(data[['Oil']])

    data['scores']=model.decision_function(data[['Oil']])
    data['anomaly']=model.predict(data[['Oil']])
    
    anomaly=data.loc[data['anomaly']==-1]
    anomaly_index=list(anomaly.index)
    print(len(data.index))
    print(len(anomaly.index))

    model= EllipticEnvelope(contamination=.02)
    model.fit(data[['Oil']])

    data['scores']=model.decision_function(data[['Oil']])
    data['anomaly']=model.predict(data[['Oil']])
    
    anomaly=data.loc[data['anomaly']==-1]
    anomaly_index=list(anomaly.index)
    print(len(data.index))
    print(len(anomaly.index))

    model=KernelDensity(bandwidth = 0.2, kernel='tophat')#gaussian
    model.fit(data[['Oil']])

    #data['scores']=model.decision_function(data[['Oil']])
    #data['anomaly']=model.predict(data[['Oil']])
    data['anomaly']=model.score_samples(data[['Oil']])
    
    anomaly=data.loc[data['anomaly']==-1]
    anomaly_index=list(anomaly.index)
    print(len(data.index))
    print(len(anomaly.index))

rawData = pd.read_csv("../../allData.csv")
formatedData = best.formatData(rawData)
calculatedData = best.manageData(formatedData)
print(calculatedData)
manageRawData(calculatedData, rawData)

#findAnomalies(calculatedData)
    