import pytest
from tasks.models import Task


@pytest.mark.django_db
def test_create_task_without_processing():
    Task.objects.create(number=123, status='created')

    assert Task.objects.count() == 1
    task = Task.objects.first()
    assert task.number == 123
    assert task.status == 'created'
