"""
"""
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from kombu import Exchange, Queue, binding

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
redis_host = os.environ.get("REDIS_HOST", default="localhost")
redis_port = os.environ.get("REDIS_PORT", default=6379)
redis_db = os.environ.get("REDIS_DB", default=0)

app = Celery(
    "project",
    broker_url= f"redis://{redis_host}:{redis_port}/{redis_db}",
)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.update(result_expires=3600, enable_utc=True, timezone="America/Sao_Paulo")


app.autodiscover_tasks()



