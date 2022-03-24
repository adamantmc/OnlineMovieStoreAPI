from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException

from auth.db.queries import get_user_by_email
from auth.password import verify_password
from auth.jwt import verify_access_token
from auth.schemas import User
from auth.db import models
from auth import schemas
from typing import Union


BearerToken = HTTPBearer()


def authenticate_user_via_credentials(user: schemas.Login) -> Union[models.User, None]:
    db_user = get_user_by_email(user.email)

    if db_user is not None and verify_password(user.password, db_user.hashed_password):
        return db_user

    return None


def authenticate_user_via_token(http_auth: HTTPAuthorizationCredentials = Depends(BearerToken)) -> Union[models.User, None]:
    payload = verify_access_token(http_auth.credentials)

    if payload is None:
        raise HTTPException(401, detail="Token expired or invalid")

    db_user = get_user_by_email(payload["email"])

    return db_user
