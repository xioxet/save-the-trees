import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Example usage
sender_email = 'savethetrees.auto@gmail.com'
sender_password = 'tvlrsnkvrazbtmcy'


def send_email(receiver_email, subject, message, sender_email=sender_email, sender_password=sender_password):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

        print('Email sent successfully!')
    except Exception as e:
        print('An error occurred while sending the email:', str(e))
    finally:
        server.quit()