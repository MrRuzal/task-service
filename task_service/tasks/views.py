from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status

from .models import Task
from .serializers import TaskSerializer
from .tasks import process_task


class TaskViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """
    ViewSet для задач. Поддерживает создание и список задач.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        """
        Создает новую задачу и запускает её обработку.
        """
        data = {
            'number': request.data.get('number'),
            'status': 'created',
        }
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            process_task.delay(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {'error': 'Недопустимые данные'},
            status=status.HTTP_400_BAD_REQUEST,
        )
