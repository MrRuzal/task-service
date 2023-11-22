# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import async_to_sync
# from .models import Task
# from .tasks import process_task


# class TaskConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         number = text_data_json['number']
#         if not number:
#             await self.send(
#                 text_data=json.dumps(
#                     {
#                         'error': 'Number is required',
#                     }
#                 )
#             )
#             return

#         task = Task.objects.create(number=number, status='created')
#         await self.send(
#             text_data=json.dumps(
#                 {
#                     'message': f'Task {task.number} created successfully.',
#                 }
#             )
#         )
#         process_task.delay(task.id)

#     @staticmethod
#     def send_task_update(event):
#         message = event['message']
#         async_to_sync(TaskConsumer.send_task_message)({'message': message})

#     async def send_task_message(self, event):
#         message = event['message']
#         await self.send(text_data=json.dumps({'message': message}))
