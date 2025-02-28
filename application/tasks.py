from celery import Celery
from celery.schedules import crontab
from image import blur_image
from mail import send_email_for_subscriber
from models import session, User

celery_app = Celery(
    "celery_app",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)


@celery_app.task
def process_image_task(image_buf: bytes, image_name: str, dir_name: str):
    """Обрабатывает изображения"""
    blur_image(image_buf, image_name, f"./{dir_name}")
    return f"{image_name} is blured"


@celery_app.task
def send_email_for_subscriber_task(receiver: str):
    """Присылает подписчику рассылку от сервера"""
    sub = session.query(User.subscription).filter(User.email == receiver).one()
    if sub:
        send_email_for_subscriber(receiver)


@celery_app.on_after_configure.connect
def setup_mailing_for_subscribers(sender, **kwargs):
    """Каждый понедельник присылает подписчику рассылку от сервера"""
    sender.add_pereodic_task(
        crontab(hour=12, minute=0, day_of_week=1),
        send_email_for_subscriber_task.s(**kwargs)
    )
