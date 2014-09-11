"""This module is used to send alert email to the fraud-engineering alias."""
import smtplib
from email.mime.text import MIMEText

MAIL_SERVER = smtplib.SMTP('mail.adnxs.net', 25)

FROM_ADDRESS = 'nobody@appnexus.com'
TO_ADDRESS = 'fruad-engineering@appnexus.com'
SUBJECT = 'monitord ALERT'
REPLY_TO = 'donotrepy@appnexus.com'


def send_alert_email(body, subject):
    """Send an email message *body* with subject *subject* to
    fraud-engineering@appnexus.com."""
    message = MIMEText(body)

    message['From'] = FROM_ADDRESS
    message['To'] = TO_ADDRESS
    message['Subject'] = subject
    message['Reply-To'] = REPLY_TO

    mime_text = MIMEText(body, 'html')
    message.attach(mime_text)

    MAIL_SERVER.sendmail(
        FROM_ADDRESS,
        TO_ADDRESS,
        message.as_string())
