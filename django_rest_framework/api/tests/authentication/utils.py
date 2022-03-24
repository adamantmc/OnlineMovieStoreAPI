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
def create_random_user() -> Tuple[str, str, User]:
    username, password = get_random_credentials()
    user_obj = User.objects.create_user(username=username, password=password)
    return username, password, user_obj


def login(client, username, password):
    r = client.post(LOGIN_URL, {"username": username, "password": password})
    assert r.status_code == 200


@pytest.fixture
def logged_in_client(client):
    u, p, user_obj = create_random_user()
    login(client, u, p)

    # Set user object in client - needed for specifying object ownership when creating
    # other objects
    client.user = user_obj

    return client
