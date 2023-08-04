import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
from flask import session
import time



# Example usage
sender_email = 'savethetrees.auto@gmail.com'
sender_password = 'tvlrsnkvrazbtmcy'


def generate_del_verification_pin():
    del_verification_pin = str(random.randint(100000, 999999))
    session['del_verification_pin'] = {
        'pin': del_verification_pin
    }
    return del_verification_pin

def generate_verification_pin():
    verification_pin = str(random.randint(100000, 999999))
    # Store the pin and its timestamp in the session
    session['verification_pin'] = {
        'pin': verification_pin,
        'timestamp': time.time()
    }
    return verification_pin

def is_verification_pin_expired():
    verification_pin_info = session.get('verification_pin')
    if verification_pin_info:
        timestamp = verification_pin_info.get('timestamp')
        return (time.time() - timestamp) >= 300  # 300 seconds = 5 minutes
    return True

def pop_verification_pin():
    session.pop('verification_pin', None)


def send_email(receiver_email, subject, message, sender_email=sender_email, sender_password=sender_password):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=120)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

        print('Email sent successfully!')
    except Exception as e:
        print('An error occurred while sending the email:', str(e))
    finally:
        server.quit()
