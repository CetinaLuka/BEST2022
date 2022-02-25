import os
from dotenv import load_dotenv
from flask_mail import Mail, Message
load_dotenv()

def createConsumptionWarning(value, date, recipients=["luka.cetina@student.um.si"], sender=os.getenv("MAIL_USERNAME")):
    msg = Message(
        subject="Poraba kurilnega olja presegla dovoljeno mejo", 
        sender=sender, 
        recipients=recipients,
        body="Dne {} je poraba kurilnega olja presegla dovoljeno mejo. Poraba je znašala {}.\nPriporočljivo je preveriti delovanje sistema, saj je lahko prišlo do poškodbe ali okvare.\n\n".format(date, value)
    )
    return msg