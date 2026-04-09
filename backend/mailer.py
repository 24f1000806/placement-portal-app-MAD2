import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


smtp_server = "localhost"
smtp_port = 1025
sender_email = "admin@gmail.com"
sender_password = ""


def send_mail(receiver, subject, message):
    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver
        msg["Subject"] = subject

        msg.attach(MIMEText(message, "html"))

        with smtplib.SMTP(host=smtp_server, port=smtp_port) as server:
            server.sendmail(sender_email, receiver, msg.as_string())

        return True
    except Exception as e:
        print("Mail sending failed:", e)
        return False


def send_admin_mail(message):
    try:
        msg = MIMEMultipart()
        msg["From"] = 'report@placementportal.com'
        msg["To"] = 'admin@gmail.com'
        msg["Subject"] = 'Monthly Placement Report'

        msg.attach(MIMEText(message, "html"))

        with smtplib.SMTP(host=smtp_server, port=smtp_port) as server:
            server.sendmail(
                'report@placementportal.com',
                'admin@gmail.com',
                msg.as_string()
            )

        return True
    except Exception as e:
        print("Admin mail sending failed:", e)
        return False