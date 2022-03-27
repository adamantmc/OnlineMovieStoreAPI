from sqlalchemy.orm import Session
from db.conn import Session


def get_session() -> Session:
    session = Session()

    try:
        yield session
    finally:
        session.close()
