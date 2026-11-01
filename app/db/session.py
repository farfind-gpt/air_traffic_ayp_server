from sqlmodel import Session

from app.db.database import ENGINE


def get_session():
    with Session(ENGINE) as session:
        yield session
