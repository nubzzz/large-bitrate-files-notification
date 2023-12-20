#!/usr/bin/env python3
"""Takes a csv input at /tmp/episodes-raw.csv, sorts by bitrate, compares against a
high bitrate env variable or defaults to 8Mb/s and sends a pushover notification
via the api"""

import http.client
from urllib import parse as urllib_parse
from os import environ
import pandas as pd

API_KEY = environ['PUSHOVER_API_KEY']
USER_KEY = environ['PUSHOVER_USER_KEY']
if environ.get('UPPER_BOUND_BITRATE') is not None:
    HIGH_BITRATE = int(environ['UPPER_BOUND_BITRATE'])
else:
    HIGH_BITRATE = 8388608
if environ['EMAIL'] == "true":
    EMAIL = True
    import smtplib
    from email.mime.text import MIMEText
    if environ['GMAIL'] == "true":
        GMAIL = True
        GMAIL_APP_PASSWORD = environ['GMAIL_APP_PASSWORD']
    else:
        print("Other email configurations are not currently supported")
        print("Email will not function")
        GMAIL = False
    if environ.get('EMAIL_RECIPIENT'):
        RECIPIENT = environ['EMAIL_RECIPIENT']
    else:
        print("EMAIL_RECIPIENT environment variable missing, you will likely experience errors")
    if environ.get('EMAIL_SENDER'):
        SENDER = environ['EMAIL_SENDER']
    else:
        print("EMAIL_SENDER environment variable missing, you will likely experience errors")

def send_email(subject, body, sender, recipients, password):
    """Sends an email using gmail"""
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

def send_pushover_notification(title, message, token, user):
    """Sends a pushover notification"""
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
        urllib_parse.urlencode({
          "token": token,
          "user": user,
          "message": message,
          "title": title
          }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()
    print("Pushover Notification sent!")

def main():
    """Main function"""
    raw_files = pd.read_csv('/tmp/episodes-raw.csv', names=['file_path','bitrate'])
    large_files = raw_files.sort_values(by=['bitrate'],ascending = False)
    large_files = large_files.loc[large_files['bitrate'] > HIGH_BITRATE]

    if large_files['file_path'].count() > 0:
        print("Large files detected")
        print("Alerting")
        title = "ALERT: Large Bitrate Files Detected"
        message = "The following files have a high bitrate.\nPlease investigate\n"
        message += '\n'.join(large_files['file_path'].to_list())
        send_pushover_notification(title, message, API_KEY, USER_KEY)
        if EMAIL and GMAIL:
            recipients = [RECIPIENT]
            send_email(title, message, SENDER, recipients, GMAIL_APP_PASSWORD)
    else:
        print("No large files detected")

if __name__ == '__main__':
    main()
