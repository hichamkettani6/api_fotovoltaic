import os
from celery import Celery

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL");
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND");

celery_app = Celery(
    'worker',
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)