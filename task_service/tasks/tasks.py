import logging
import time
from datetime import datetime, timedelta

from celery import shared_task
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Task

logger = logging.getLogger(__name__)

OLD_TASKS_THRESHOLD = timedelta(minutes=10)


def get_task(task_id):
    """
    Получает объект задачи по идентификатору.
    """
    try:
        return Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        message = f'Задача с идентификатором {task_id} не существует.'
        logger.warning(message)
        raise ValueError(message)


@shared_task
def process_task(task_id):
    """
    Запускает обработку задачи по её идентификатору и проверяет статус.
    """
    task = get_task(task_id)
    if task.status == 'created':
        process_created_task.delay(task_id)
    message = f'Статус задачи {task_id} не является "created".'
    logger.warning(message)
    raise ValueError(message)


@shared_task
def process_created_task(task_id):
    """
    Обрабатывает задачу со статусом 'created'.
    """
    task = get_task(task_id)
    task.status = 'processing'
    task.save()
    logger.info(f'Задача {task_id} находится в обработке...')

    # Предположим, что обработка задачи занимает 10 секунд
    # Можно заменить этот код на свою логику
    time.sleep(10)
    complete_task.delay(task_id)


@shared_task
def complete_task(task_id):
    """
    Завершает обработку задачи и отправляет уведомление.
    """
    from .consumers import TaskConsumer

    task = get_task(task_id)
    task.status = 'completed'
    task.save()
    logger.info(f'Задача {task_id} успешно завершена.')
    TaskConsumer().send_task_update(
        {
            'message': f'Задача {task_id} успешно завершена.',
        }
    )


@receiver(post_save, sender=Task)
def process_task_on_creation(sender, instance, created, **kwargs):
    """
    Обработчик сигнала для запуска обработки задачи при её создании.
    """
    if created:
        process_task.delay(instance.id)


@shared_task
def delete_old_tasks():
    """
    Удаляет задачи, созданные более семи дней назад.
    """
    seven_days_ago = datetime.now() - OLD_TASKS_THRESHOLD
    old_tasks = Task.objects.filter(created_at__lt=seven_days_ago)
    old_tasks.delete()


@shared_task
def retry_stuck_tasks():
    """
    Повторно запускает подвисшие задачи.
    """
    stuck_tasks = Task.objects.filter(status__in=['created', 'processing'])
    for task in stuck_tasks:
        if task.status == 'created':
            process_task.delay(task.id)
        elif task.status == 'processing':
            process_created_task.delay(task.id)
