import logging
import time
from datetime import datetime, timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver
from django_rq import job

from .models import Task

logger = logging.getLogger(__name__)


@job
def process_task(task_id):
    """
    Запускает обработку задачи по её идентификатору и проверяет статус.
    """
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        message = f'Задача с идентификатором {task_id} не существует.'
        logger.warning(message)
        raise ValueError(message)

    if task.status == 'created':
        process_created_task(task)
    message = f'Статус задачи {task.number} не является "created".'
    logger.warning(message)
    raise ValueError(message)


def process_created_task(task):
    """
    Обрабатывает задачу со статусом 'created'.
    """
    task.status = 'processing'
    task.save()
    logger.info(f'Задача {task.number} находится в обработке...')

    # Предположим, что обработка задачи занимает 10 секунд
    # Можно заменить этот код на свою логику
    time.sleep(10)

    complete_task(task)


def complete_task(task):
    """
    Завершает обработку задачи и отправляет уведомление.
    """
    from .consumers import TaskConsumer

    task.status = 'completed'
    task.save()
    logger.info(f'Задача {task.number} успешно завершена.')
    TaskConsumer().send_task_update(
        {
            'message': f'Задача {task.number} успешно завершена.',
        }
    )


@receiver(post_save, sender=Task)
def process_task_on_creation(sender, instance, created, **kwargs):
    """
    Обработчик сигнала для запуска обработки задачи при её создании.
    """
    if created:
        process_task.delay(instance.id)


@job
def delete_old_tasks():
    """
    Удаляет задачи, созданные более семи дней назад.
    """
    seven_days_ago = datetime.now() - timedelta(days=7)
    old_tasks = Task.objects.filter(created_at__lt=seven_days_ago)
    old_tasks.delete()
