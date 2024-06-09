from celery import Celery
from app.celery_tasks.celery_schedule import schedules as task_schedules
from app.config import settings

app = Celery(
    "app",
    broker=settings.CELERY_BROKER,
    backend=settings.CELERY_BACKEND,
    timezone=settings.TIMEZONE,
    task_serializer="json",
    result_serializer="json",
    task_time_limit=3600,
    task_acks_late=True,
)
app.autodiscover_tasks(packages=["app.celery_tasks"])
app.conf.beat_schedule = task_schedules
