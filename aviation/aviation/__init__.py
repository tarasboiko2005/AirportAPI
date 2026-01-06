from .celery import app as celery_app
from aviation import tasks
__all__ = ("celery_app",)