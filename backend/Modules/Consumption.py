from numpy import double
import pandas as pd
import Modules.best2022 as best
from flask_mail import Mail
from dotenv import load_dotenv
import Modules.MailTemplates as mail_temp
import os
load_dotenv()

def checkIfConsumptionIsWithinRange(row:pd.DataFrame, mail:Mail):
    MAX_CONSUMPTION = os.getenv('MAX_CONSUMPTION')
    if(row["Diff"] > float(MAX_CONSUMPTION)):
        #TODO pošlji email obvestilo da je poraba presegla threshold
        print("Pošlji mail, kjer je poraba več kot MAX_CONSUMPTION poraba je:", row["Diff"])
        msg = mail_temp.createConsumptionWarning(round(row["Diff"]*1000, 2), row["Date"].strftime("%d %b %Y"))
        mail.send(msg)
        print("Obvestilo poslano")


#data = pd.read_csv("./Data/allData.csv")
#data = best.formatData(data)
#managedData = best.manageData(data)
#for index, row in managedData.iterrows():
    #checkIfConsumptionIsWithinRange(row)
    