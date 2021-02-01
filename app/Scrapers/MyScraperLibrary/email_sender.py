import smtplib, ssl
from email.message import EmailMessage

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
my_gmail = "nicolae.filat@gmail.com"  # Enter your address
receiver_email = "nicolae.filat@gmail.com"
password = "N2002ife524"
message = """\
Subject: Buna mami,
Am ga

This message is sent from Python."""



def send_message(message, to_self = False,destinatator = None):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(my_gmail, password)
        msg = EmailMessage()
        msg['Subject'] = "Vaccin gasit!"
        msg['From'] = my_gmail
        if to_self:
            destinatator = my_gmail
        msg['To'] = destinatator
        msg.set_content(message)
        server.send_message(msg)