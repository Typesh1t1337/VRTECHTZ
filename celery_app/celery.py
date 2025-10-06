from celery import Celery
from config import settings

celery_app = Celery(
    "updater",
    broker=settings.CELERY_BROKER,
    backend=settings.CELERY_RESULT,
    include=["celery_app.tasks"]
)

celery_app.conf.beat_schedule = {
    "update-every-15-minutes": {
        "task": "celery_app.tasks.update_products",
        "schedule": 15 * 60.0,
    }
}

celery_app.conf.timezone = "UTC"
