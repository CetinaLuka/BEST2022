import os
from dotenv import load_dotenv
from flask_mail import Mail, Message
from flask import render_template
load_dotenv()

def createConsumptionWarning(value, date, recipients=[os.getenv('WARNING_RECIPIENT')], sender=os.getenv("MAIL_USERNAME")):
    msg = Message(
        subject="Poraba kurilnega olja presegla dovoljeno mejo", 
        sender=sender, 
        recipients=recipients,
    )
    msg.html = render_template("obvestilo_o_preveliki_porabi.html", date=date, allowed=float(os.getenv('MAX_CONSUMPTION'))*1000, consumption=value)
    return msg


def createRefilWarning(value, date, amount, recipients=[os.getenv('WARNING_RECIPIENT')], sender=os.getenv("MAIL_USERNAME")):
    msg = Message(
        subject="Dolivanje kurilnega olja",
        sender=sender,
        recipients=recipients,
    )
    msg.html = render_template("zaznano_polnjenje.html", date=date, amount=amount, consumption=value)
    return msg