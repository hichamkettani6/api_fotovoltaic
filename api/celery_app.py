import os
import requests
from celery import Celery
import logging
import redis

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")
REDIS_URL = os.environ.get("REDIS_URL")
TZ = os.environ.get("TZ")

redis_client = redis.Redis.from_url(REDIS_URL)


celery_app = Celery(
    'worker',
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)

celery_app.conf.beat_schedule = {
    "fetch-weather-every-10-seconds": {
        "task": "celery_app.fetch_weather",
        "schedule": 2.0,
    },
}

celery_app.conf.timezone = TZ



@celery_app.task
def fetch_weather():
    try:
        response = requests.get(
            'https://api.open-meteo.com/v1/forecast?latitude=45.0134016&longitude=7.6447744&current_weather=true'
        )
        data = response.json()
        temperature = data['current_weather']['temperature']
        message = f"{temperature}°C"
        redis_client.publish('weather', message)
    except Exception as e:
        logger.error("Error fetching weather data: %s", str(e))
        redis_client.publish('weather', 'Error loading weather data!')
