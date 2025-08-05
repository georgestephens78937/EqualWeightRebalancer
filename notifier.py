from config import Config
from email.message import EmailMessage
from smtplib import SMTP_SSL

class Notifier:
    def __init__(self, config: Config):
        self.sender = config.email_sender
        self.password = config.email_password
        self.receiver = config.email_receiver
    
    def send(self, subject: str, body: str):
        try:
            if not all([self.sender, self.password, self.receiver]):
                print("\nError: Missing email configuration information")
                return
            
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = self.sender
            msg['To'] =self.receiver
            msg.set_content(body)

            with SMTP_SSL('smtp.gmail.com', 465) as stmp:
                stmp.login(self.sender, self.password)
                stmp.send_message(msg)

            print('Email sent.')

        except Exception as e: print(f'Failed to send email: {e}')

    def error_send(self, e: str):
        try:
            if not all([self.sender, self.password, self.receiver]):
                print("\nError: Missing email configuration information")
                return
            
            msg = EmailMessage()
            msg['Subject'] = 'Error Executing Rebalancer'
            msg['From'] = self.sender
            msg['To'] =self.receiver
            msg.set_content(e)

            with SMTP_SSL('smtp.gmail.com', 465) as stmp:
                stmp.login(self.sender, self.password)
                stmp.send_message(msg)

            print('Error Email sent.')

        except Exception as e: print(f'Failed to send error email: {e}')