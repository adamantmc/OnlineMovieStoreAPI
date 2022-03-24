from auth.db import models
from db.conn import Session


def create_user(username: str, email: str, hashed_password: str) -> models.User:
    with Session(expire_on_commit=False) as session:
        u = models.User(username=username, email=email, hashed_password=hashed_password)
        session.add(u)
        session.commit()

        return u


def get_user_by_email(email) -> models.User:
    with Session(expire_on_commit=False) as session:
        u = session.query(models.User).filter(models.User.email == email).first()

        return u
