from tests.authentication.utils import *
import pytest

LOGIN_URL = "/auth/login/"


@pytest.mark.django_db
def test_login(client):
    u, p = create_random_user()
    r = client.post(LOGIN_URL, {"username": u, "password": p})
    assert r.status_code == 200
