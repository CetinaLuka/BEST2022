from flask import Flask, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
import Modules.Consumption as consumption
import Modules.Utils as Utils
import Modules.DetectRefills as detectRefill
import Modules.best2022 as best
import Modules.dataBase_util as db

load_dotenv()

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.getenv('MAIL_USERNAME'),
    "MAIL_PASSWORD": os.getenv('MAIL_PASSWORD')
}

app = Flask(__name__)

app.config.update(mail_settings)
mail = Mail(app)

@app.route('/')
def hello_world():
    print(app.config)
    return 'Hello World!!!!!'

@app.route('/import')
def importMeasurements():
    best.mergeFiles()
    data = best.readPrevData() 
    print(data)
    data = detectRefill.manageRawData(data)
    print(data)
    db.csvToAccess(data)
    return data.to_string()
    
@app.route('/email')
def sendMail():
    with app.app_context():
        print("sending mail")
        msg = Message(
            subject="Test", 
            sender=app.config.get("MAIL_USERNAME"), 
            recipients=["luka.cetina@student.um.si"], 
            body="Test emaila"
        )
        mail.send(msg)
        print("mail sent");
    return "email poslan"

@app.route('/consumption')
def checkConsumption():
    print("test")
    with app.app_context():
        managedData = Utils.getmanagedData();
        consumption.checkIfConsumptionIsWithinRange(managedData.iloc[-1], mail)
    return "Checked consumption"

    

if __name__ == '__main__':
    app.run()