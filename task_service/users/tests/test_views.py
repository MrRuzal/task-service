import pytest
from rest_framework.test import APIClient
from rest_framework import status
from users.models import CustomUser


@pytest.mark.django_db
def test_user_creation_view():
    client = APIClient()
    url = 'http://localhost:8000/api/users/'  # локальный тест
    data = {
        'email': 'test@example.com',
        'username': 'testuser',
        'password': 'testpassword',
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    user = CustomUser.objects.get(email='test@example.com')
    assert user.username == 'testuser'
