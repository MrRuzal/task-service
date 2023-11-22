import pytest
from users.models import CustomUser


@pytest.mark.django_db
def test_create_user():
    user = CustomUser.objects.create_user(
        email='test@example.com', username='testuser', password='testpassword'
    )
    assert user.email == 'test@example.com'
    assert user.username == 'testuser'
    assert user.check_password('testpassword')
