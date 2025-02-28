from dotenv import load_dotenv, find_dotenv
import os

if not find_dotenv():
    exit("Переменные окружения не найдены")
else:
    load_dotenv()

SMTP_USER = os.getenv("SMTP_USER")
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_PORT = os.getenv("SMTP_PORT")
