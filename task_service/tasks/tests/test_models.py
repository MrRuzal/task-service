import pytest
from tasks.models import Task


@pytest.mark.django_db
def test_create_task():
    task = Task.objects.create(number=123, status='created')
    assert Task.objects.count() == 1
    assert task.number == 123
    assert task.status == 'created'
