import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'steambroproject.settings')

app = Celery('steambroproject')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscovery_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Requests: {self.request!r}')
