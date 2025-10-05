from celery import Celery
from config import settings

celery_app = Celery(
    "updater",
    broker=settings.CELERY_BROKER,
    backend=settings.CELERY_RESULT,
)

celery_app.conf.beat_schedule = {
    "update-every-15-minutes": {
        "task": "",
        "schedule": 15 * 60,
    }
}
