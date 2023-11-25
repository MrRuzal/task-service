from django.db import IntegrityError
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer
from .tasks import process_task


class TaskViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """
    ViewSet для задач. Поддерживает создание, запуск обработки и список задач.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            process_task.delay(serializer.data['id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
