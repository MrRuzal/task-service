import pytest
from users.serializers import UserSerializer


@pytest.mark.django_db
def test_user_serializer():
    data = {
        'email': 'test@example.com',
        'username': 'testuser',
        'password': 'testpassword',
    }
    serializer = UserSerializer(data=data)
    assert serializer.is_valid()
    user = serializer.save()
    assert user.email == 'test@example.com'
    assert user.username == 'testuser'
    assert user.check_password('testpassword')
