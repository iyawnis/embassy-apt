# -*- coding: utf-8 -*-

import json
import smtplib
import os
from lxml import html
import requests
from datetime import datetime

RESERVATION_XPATH = '//*[@id="dnn_ctr484_MakeReservation_availabilityRepeater_availabilityLabel_2"]'
EMBASSY_URL = 'https://www.greekembassy.org.uk/el-gr/Reservations'

gmail_user = os.environ['GMAIL_USER']
gmail_pwd = os.environ['GMAIL_PASSWORD']

def send_email(text):

    FROM = gmail_user
    TO = [gmail_user]
    SUBJECT = 'Embasy appointments'
    TEXT = text

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
    except:
        return False
    return True


def lambda_handler(event, context):
    page = requests.get(EMBASSY_URL)
    tree = html.fromstring(page.content)
    appointments = tree.xpath(RESERVATION_XPATH)

    if not u'δεν υπάρχει Διαθεσιμότητα.' in appointments[0].text_content():
        print(datetime.now().isoformat(), 'Appointments available!')
        send_email('Available appointments')
        return {
            'statusCode': 201,
            'body': json.dumps('Available appointments')
        }
    else:
        print(datetime.now().isoformat(), "No Appointments")
        return {
            'statusCode': 200,
            'body': json.dumps('No available appointments')
        }

if __name__ == '__main__':
    lambda_handler(None, None)
