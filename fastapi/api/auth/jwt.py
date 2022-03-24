from auth.db import models
from typing import Union
import jwt

SECRET_KEY = "secret"
ALGORITHM = "HS256"


def get_payload_for_user(user: models.User) -> dict:
    return {
        "username": user.username,
        "uuid": user.uuid,
        "email": user.email,
    }


def create_access_token(user: models.User) -> str:
    payload = get_payload_for_user(user)

    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(access_token: str) -> Union[dict, None]:
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.exceptions.PyJWTError:
        payload = None

    return payload
