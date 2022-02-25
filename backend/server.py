import Modules.best2022 as best
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/import')
def importMeasurements():
    return best.importAccess()
    

def sendMail():
    print("sending mail");

if __name__ == '__main__':
    app.run()