# import logging
# from datetime import datetime, timedelta
# from django_rq import job
# from asgiref.sync import async_to_sync
# from .models import Task
# from .consumers import TaskConsumer

# logger = logging.getLogger(__name__)


# @job
# def process_task(task_id):
#     try:
#         task = Task.objects.get(id=task_id)

#         if task.status == 'created':
#             task.status = 'processing'
#             task.save()

#             # Код обработки задачи
#             # ...

#             # Предположим, что обработка задачи занимает 5 секунд
#             # Вы можете заменить этот код на свою логику
#             import time

#             time.sleep(5)

#             # Обработка завершена, меняем статус на "завершена"
#             task.status = 'completed'
#             task.save()

#             # Отправляем сообщение обновления через WebSocket
#             TaskConsumer().send_task_update(
#                 {
#                     'message': f'Task {task.number} completed successfully.',
#                 }
#             )

#     except Task.DoesNotExist:
#         logger.warning(f"Задача с идентификатором {task_id} не существует.")
#         raise ValueError(f"Задача с идентификатором {task_id} не существует.")


# @job
# def delete_old_tasks():
#     seven_days_ago = datetime.now() - timedelta(days=7)
#     old_tasks = Task.objects.filter(created_at__lt=seven_days_ago)
#     old_tasks.delete()
