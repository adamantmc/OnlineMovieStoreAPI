from sqlalchemy import String, Integer, DateTime, Column
from db.conn import Base
import datetime
import uuid


def get_current_datetime() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String, default=lambda: str(uuid.uuid4()), unique=True)

    username = Column(String)
    email = Column(String, unique=True)

    hashed_password = Column(String)

    registered_at = Column(DateTime, default=get_current_datetime)
