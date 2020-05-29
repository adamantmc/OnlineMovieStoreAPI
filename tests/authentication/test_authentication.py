from tests.authentication.utils import *
import pytest


@pytest.mark.django_db
def test_login(client):
    u, p = create_random_user()
    r = client.post(LOGIN_URL, {"username": u, "password": p})
    assert r.status_code == 200


@pytest.mark.django_db
def test_login_missing_credentials(client):
    r = client.post(LOGIN_URL, {})
    assert r.status_code == 400
    r = client.post(LOGIN_URL, {"username": "", "password": ""})
    assert r.status_code == 400


@pytest.mark.django_db
def test_login_invalid_credentials(client):
    u, p = get_random_credentials()
    r = client.post(LOGIN_URL, {"username": u, "password": p})
    assert r.status_code == 400


@pytest.mark.django_db
def test_auth_cookie_set(client):
    u, p = create_random_user()
    r = client.post(LOGIN_URL, {"username": u, "password": p})
    assert r.status_code == 200

    assert "auth" in client.cookies

    auth_cookie = client.cookies["auth"]

    assert auth_cookie["httponly"]


@pytest.mark.django_db
def test_logout(logged_in_client, a="asd"):
    r = logged_in_client.get(LOGOUT_URL)
    assert r.status_code == 200

    assert "auth" in logged_in_client.cookies
    assert logged_in_client.cookies["auth"].value == ""


def test_logout_without_login(client):
    r = client.get(LOGOUT_URL)
    assert r.status_code == 401

