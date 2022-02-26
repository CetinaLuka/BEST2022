import Modules.best2022 as best
import Modules.dataBase_util as db
from flask import Flask, jsonify, render_template
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
import Modules.Consumption as consumption
import Modules.Utils as Utils
from flask_apscheduler import APScheduler

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
app=Flask(__name__,template_folder='template')
app.config.update(mail_settings)
mail = Mail(app)

scheduler = APScheduler()
scheduler.init_app(app)

# izvede se vsak dan 5 minut čez polnoč
@scheduler.task('cron', id='dnevno_branje_nove_datoteke', hour=00, minute=5)
def daily_file_import():
    print('Job 1 executed')

# izvede se v 30 sekundah potem, ko se aplikacija zažene
#@scheduler.task('interval', id='demo_branje_nove_datoteke', seconds=30)
#def daily_file_import_demo():
#    print('Job 1 executed')

def run_on_start():
    print("reading old files")
    best.readOldFiles()

@app.route('/')
def hello_world():
    return 'Hello World!!!!!'

@app.route('/import')
def importMeasurements():
    best.mergeFiles()
    data = best.readPrevData() 
    print(data)
    db.csvToAccess(data)
    return data.to_string()
    
@app.route('/email')
def sendMail():
    with app.app_context():
        print("sending mail");
        msg = Message(
            subject="Test", 
            sender=app.config.get("MAIL_USERNAME"), 
            recipients=["luka.cetina@student.um.si"], 
        )
        msg.html = render_template("obvestilo_o_preveliki_porabi.html", date="30/10/2022", allowed=10, consumption=12.9)
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

    
scheduler.start()
#run_on_start()

if __name__ == '__main__':
    app.run()
    