from typing import Tuple
from django.contrib.auth.models import User
import pytest
from tests.common.utils import get_random_string


LOGIN_URL = "/auth/login/"
LOGOUT_URL = "/auth/logout/"


def get_random_credentials() -> Tuple[str, str]:
    username = get_random_string(16)
    password = get_random_string(16)

    return username, password


@pytest.mark.django_db
def create_random_user() -> Tuple[str, str]:
    username, password = get_random_credentials()
    User.objects.create_user(username=username, password=password)
    return username, password


@pytest.fixture
def logged_in_client(client):
    u, p = create_random_user()
    r = client.post(LOGIN_URL, {"username": u, "password": p})
    assert r.status_code == 200

    return client
