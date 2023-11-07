import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "celery_beat.settings")

app = Celery("currency", broker="amqp://guest:guest@localhost//")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.update(
    broker_connection_retry_on_startup=True,  # Set this to enable broker connection retries on startup
    # Add other necessary configurations as needed
)

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "add-every-10sec": {
        "task": "currency.tasks.pull_rate",
        "schedule": crontab(minute=0, hour="*/4"),
    },
}
