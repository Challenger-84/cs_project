import os
import smtplib

from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASS')

smtp =  smtplib.SMTP('smtp.gmail.com', 587)
smtp.ehlo()
smtp.starttls()
smtp.ehlo()
smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

def send_mail(reciever, subject, body):
    msg = f'Subject: {subject}\n\n {body}'
    smtp.sendmail(EMAIL_ADDRESS, reciever, msg)