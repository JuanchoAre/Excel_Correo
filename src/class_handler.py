import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from loguru import logger

class Excel_Handler:
    def __init__(self):
        pass

    def read_excel(self, file):
        try:
            df = pd.read_excel(file)
            return df
        except Exception as e:
            print(f"Error al leer el excel: {e}")
            return None

    def excel_to_list(self, file_path):
        df = pd.read_excel(file_path, header=0)
        df = df.iloc[:]
        list_ = df.values.tolist()
        return list_

class Email_Handler:
    def __init__(self, smtp_server='smtp.gmail.com', smtp_port=587, username='', password=''):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send_email(self, email_list):
        # Aquí iría la lógica para enviar el correo
        try:
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = email_list[1]
            msg['Subject'] = email_list[0]
            msg.attach(MIMEText(f"Su deuda a pagar es de {email_list[2]}", 'plain'))
        except Exception as e:
            print(f"Error al crear el mensaje: {e}")
            return False
        # Por ejemplo, usando smtplib o cualquier otra librería de envío de correos
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.sendmail(self.username, email_list[1], msg.as_string())
                logger.info(f"Correo enviado a {email_list[1]}")
            return True
        except Exception as e:
            logger.error(f"Error al enviar el correo: {e}")
            return False