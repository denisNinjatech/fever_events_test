from celery import Celery
from decouple import AutoConfig
import os

# Set up the base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env file
config = AutoConfig(search_path=BASE_DIR)

celery_app = Celery(
    'fever_event',
    broker='redis://localhost:6379/0',  # Redis broker URL
    backend='redis://localhost:6379/0'  # Redis backend URL
)

celery_app.conf.beat_schedule = {
    'fetch-events-every-minute': {
        'task': 'fever_event.tasks.scheduled_fetch',
        'schedule': int(config("Interval")) if config("Interval") else 60,  # Run every minute
    },
}

celery_app.conf.timezone = 'UTC'
celery_app.autodiscover_tasks(['fever_event.tasks'])