import os

from celery import Celery

from datetime import timedelta

DELETE_OLD_TASKS_SCHEDULE = timedelta(minutes=10)
RETRY_STUCK_TASKS_SCHEDULE = timedelta(minutes=1)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_service.settings')

app = Celery('task_service')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete_old_tasks': {
        'task': 'tasks.tasks.delete_old_tasks',
        'schedule': DELETE_OLD_TASKS_SCHEDULE,
    },
    'retry_stuck_tasks': {
        'task': 'tasks.tasks.retry_stuck_tasks',
        'schedule': RETRY_STUCK_TASKS_SCHEDULE,
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
