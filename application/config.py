import os

from dotenv import find_dotenv, load_dotenv

if not find_dotenv():
    exit("Переменные окружения не найдены")
else:
    load_dotenv()

SMTP_USER = os.getenv("SMTP_USER")
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_PORT = os.getenv("SMTP_PORT")
DB_PATH = os.getenv("DB_PATH")
