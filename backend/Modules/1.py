import pandas as pd
import best2022 as best

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
    


rawData = pd.read_csv("../../allData.csv")
formatedData = best.formatData(rawData)
calculatedData = best.manageData(formatedData)
print(calculatedData)
manageRawData(calculatedData, rawData)
    