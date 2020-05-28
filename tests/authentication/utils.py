from typing import Tuple
from django.contrib.auth.models import User
import pytest
import random
import string


def get_random_credentials() -> Tuple[str, str]:
    chars = string.ascii_letters + string.digits

    username = "".join([random.choice(chars) for i in range(16)])
    password = "".join([random.choice(chars) for i in range(16)])

    return username, password


@pytest.mark.django_db
def create_random_user() -> Tuple[str, str]:
    username, password = get_random_credentials()
    User.objects.create_user(username=username, password=password)
    return username, password
