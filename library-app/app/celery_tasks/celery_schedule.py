from celery.schedules import crontab

schedules = {
    "send_return_reminders": {
        "task": "app.celery_tasks.tasks.send_return_reminders",
        "schedule": crontab(minute="5", hour="3"),
    },
    "generate_weekly_report": {
        "task": "app.celery_tasks.tasks.generate_weekly_report",
        "schedule": crontab(hour="5", minute="0", day_of_week="1"),
    },
}
