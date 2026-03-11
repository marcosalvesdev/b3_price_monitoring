import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.broker_url = os.getenv("CELERY_BROKER_URL")
app.conf.result_backend = os.getenv("CELERY_RESULT_BACKEND")

app.autodiscover_tasks()
app.autodiscover_tasks(["globals"])
