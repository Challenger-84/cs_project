import os
import smtplib

from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASS')

with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    subject = 'test'
    body = 'this is a test'

    msg = f'Subject: {subject}\n\n {body}'

    smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)