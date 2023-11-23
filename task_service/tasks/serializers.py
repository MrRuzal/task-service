from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Task.

    Поля:
    - id: Идентификатор задачи.
    - number: Номер задачи.
    - status: Статус задачи.
    - created_at: Время создания задачи.
    - updated_at: Время последнего обновления задачи.
    """

    class Meta:
        model = Task
        fields = ['id', 'number', 'status', 'created_at', 'updated_at']
