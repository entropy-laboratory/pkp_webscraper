import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# import sys
# import io

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class EmailSender:
    def __init__(self, gmail_user, gmail_password):
        self.gmail_user = gmail_user
        self.gmail_password = gmail_password

    def send_email(self, to_email, subject, body):
        message = MIMEMultipart()
        message["From"] = self.gmail_user
        message["To"] = to_email
        message["Subject"] = subject

        message.attach(MIMEText(body, "html"))

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.gmail_user, self.gmail_password)
                server.sendmail(self.gmail_user, to_email, message.as_string())
            print("📧 E-mail wysłany pomyślnie.")
        except Exception as e:
            print(f"❌ Błąd przy wysyłaniu e-maila: {e}")
