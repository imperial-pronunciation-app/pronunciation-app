from typing import Generator, Iterator

from fastapi import Depends
from fastapi_users_db_sqlmodel import SQLModelUserDatabase
from sqlmodel import Session, create_engine

from app.config import get_database_url
from app.models.user import User


engine = create_engine(get_database_url())

def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session

def get_user_db(session: Session = Depends(get_session)) -> Generator[SQLModelUserDatabase, None, None]:
    yield SQLModelUserDatabase(session, User)
