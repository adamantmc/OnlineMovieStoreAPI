from tests.authentication.utils import *
import pytest

LOGIN_URL = "/auth/login/"


@pytest.mark.django_db
def test_login(client):
    create_user("user", "user")
    from django.contrib.auth.models import User
    print(User.objects.all())
    r = client.post(LOGIN_URL, {"username": "user", "password": "user"})
    assert r.status_code == 200