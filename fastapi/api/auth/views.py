from fastapi import APIRouter, HTTPException
from auth.db.queries import create_user
from auth import schemas

from auth.password import hash_password
from auth.authentication import authenticate_user_via_credentials
from auth.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register/", response_model=schemas.User)
async def register(user: schemas.CreateUser):
    user = create_user(username=user.username, email=user.email, hashed_password=hash_password(user.password))
    return user


@router.post("/login/", response_model=schemas.AccessToken)
async def login(login_info: schemas.Login):
    user = authenticate_user_via_credentials(login_info)

    if user is None:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token(user)

    return schemas.AccessToken(access_token=token)
