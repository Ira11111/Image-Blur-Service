import io
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from config import SMTP_HOST, SMTP_PORT, SMTP_PASSWORD, SMTP_USER


def send_email(order_id: str, receiver: str, zip_file: bytes, filename: str = "new_images.zip"):
    """
    Отправляет пользователю `receiver` письмо по заказу `order_id` с приложенным файлом `filename`

    Вы можете изменить логику работы данной функции
    """
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)

        email = MIMEMultipart()
        email['Subject'] = f'Изображения. Заказ №{order_id}'
        email['From'] = SMTP_USER
        email['To'] = receiver

        with io.BytesIO(zip_file) as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= blur_images.zip",
            )
            email.attach(part)

        text = email.as_string()

        server.sendmail(SMTP_USER, receiver, text)


def send_email_for_subscriber(receiver: str):
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)

        email = MIMEMultipart()
        email["Subject"] = "Еженедельная рассылка для подписчиков"
        email["From"] = SMTP_USER
        email["To"] = receiver

        text = email.as_string("wjfrnfjrn")

        server.sendmail(SMTP_USER, receiver, text)
