import celery
from celery import Celery, group
from celery.schedules import crontab
from image import blur_image
from mail import send_email_for_subscriber
from archive import create_archive
from models import session, User

celery_app = Celery(
    "celery_app",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)
celery_app.conf.beat_max_loop_interval = 60


@celery_app.task
def process_image_task(image_buf: bytes, image_name: str, dir_name: str):
    """Обрабатывает изображения"""
    try:
        blur_image(image_buf, image_name, f"./{dir_name}")
    except Exception as e:
        print(f"Error in processing image {image_name}: {e}")
        return
    return f"{image_name} is blured"


@celery_app.task
def create_archive_task(path: str):
    return create_archive(path)


@celery_app.task
def send_email_for_subscriber_task(receiver: str):
    """Присылает подписчику рассылку от сервера"""
    try:
        send_email_for_subscriber(receiver)
        print(f"Email sent to {receiver}")
    except Exception as e:
        print(f"Error sending email to {receiver}: {e}")


@celery.shared_task
def send_email_for_all_subscribers_task():
    """Отправляет рассылку всем подписчикам"""
    try:
        emails = session.query(User.email).filter(User.subscription == True).all()
        print(f"Found emails: {list(emails)}")
        task_group = group(
            send_email_for_subscriber_task.s(email[0]) for email in emails
        )
        task_group.apply_async()
    except Exception as e:
        print(f"Error in send_email_for_all_subscribers_task: {e}")
    finally:
        session.close()


@celery_app.on_after_configure.connect
def setup_mailing_for_subscribers(sender, **kwargs):
    """Рассылка каждый понедельник в 12:00"""
    sender.add_periodic_task(
        crontab(hour=12, minute=0, day_of_week=1),
        send_email_for_all_subscribers_task.s(),
    )
