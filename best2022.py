import os


mainFileName = "allData.txt"
os.remove(mainFileName)

allData = open(mainFileName, "a+")

path = 'Arhiv_2021'
arr = os.listdir(path)
for folder in arr:
    arrFile = os.listdir(path + "/" + folder)
    fileName = arrFile[0]
    currFile = open(path + "/" + folder + "/" + fileName, "r")
    allData.write(currFile.read())
    currFile.close()