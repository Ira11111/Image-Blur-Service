import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import SMTP_HOST, SMTP_PASSWORD, SMTP_PORT, SMTP_USER


def send_email(order_id: str, receiver: str, zip_file: bytes):
    """
    Отправляет пользователю `receiver` письмо
    по заказу `order_id` с приложенным файлом
    """
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)

        email = MIMEMultipart()
        email["Subject"] = f"Изображения от ImageBlur. Заказ №{order_id}"
        email["From"] = SMTP_USER
        email["To"] = receiver

        with open(zip_file, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                "attachment; filename= blur_images.zip",
            )
            email.attach(part)

        text = email.as_string()

        server.sendmail(SMTP_USER, receiver, text)


def send_email_for_subscriber(receiver: str):
    """Отправляет письма для подписчиков"""
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)

        email = MIMEMultipart()
        email["Subject"] = "Еженедельная рассылка для подписчиков от ImageBlur"
        email["From"] = SMTP_USER
        email["To"] = receiver

        text = "Здесь могла быть ваша реклама"
        email.attach(MIMEText(text, "plain", "utf-8"))

        server.sendmail(SMTP_USER, receiver, email.as_string())
