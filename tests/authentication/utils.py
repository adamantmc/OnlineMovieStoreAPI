import pytest
from typing import Tuple
from django.contrib.auth.models import User


@pytest.mark.django_db
def create_user(username: str, password: str):
    User.objects.create_user(username, password)