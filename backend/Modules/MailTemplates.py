import os
from dotenv import load_dotenv
from flask_mail import Mail, Message
from flask import render_template
load_dotenv()

def createConsumptionWarning(value, date, recipients=["luka.cetina@student.um.si"], sender=os.getenv("MAIL_USERNAME")):
    msg = Message(
        subject="Poraba kurilnega olja presegla dovoljeno mejo", 
        sender=sender, 
        recipients=recipients,
        body="Dne {} je poraba kurilnega olja presegla dovoljeno mejo. Poraba je znašala {}.\nPriporočljivo je preveriti delovanje sistema, saj je lahko prišlo do poškodbe ali okvare.\n\n".format(date, value)
    )
    msg.html = render_template("obvestilo_o_preveliki_porabi.html", date=date, allowed=os.getenv('MAX_CONSUMPTION'), consumption=value)
    return msg


def createRefilWarning(value, date, recipients=["luka.cetina@student.um.si"], sender=os.getenv("MAIL_USERNAME")):
    msg = Message(
        subject="Dolivanje kurilnega olja", 
        sender=sender, 
        recipients=recipients,
        body="Dne {} se je dolilo korilno olje. Dolilo se je {}.\n\n".format(date, value)
    )
    return msg