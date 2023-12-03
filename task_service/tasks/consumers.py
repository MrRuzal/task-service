import json

from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Task
from .tasks import process_task


class TaskConsumer(AsyncWebsocketConsumer):
    """
    Consumer для обработки WebSocket-подключений для задач.
    """

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        number = text_data_json['number']
        if not number:
            await self.send(
                text_data=json.dumps(
                    {
                        'error': 'Номер обязателен',
                    }
                )
            )
            return
        task = Task.objects.create(number=number, status='created')
        await self.send(
            text_data=json.dumps(
                {
                    'message': f'Задача {task.number} успешно завершена.',
                }
            )
        )
        process_task.delay(task.id)

    async def send_task_update(self, event):
        """
        Отправляет обновление о состоянии задачи клиенту.
        """
        message = event['message']
        await self.send_task_message({'message': message})

    async def send_task_message(self, event):
        """
        Отправляет сообщение о состоянии задачи клиенту.
        """
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))
