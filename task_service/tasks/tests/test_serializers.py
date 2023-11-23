import pytest
from tasks.models import Task
from tasks.serializers import TaskSerializer


@pytest.mark.django_db
def test_task_serializer():
    task = Task.objects.create(number=123, status='created')
    serializer = TaskSerializer(instance=task)
    assert serializer.data['number'] == 123
    assert serializer.data['status'] == 'created'
