import os
from typing import Generator, Iterator

from dotenv import load_dotenv
from fastapi import Depends
from fastapi_users_db_sqlmodel import SQLModelUserDatabase
from sqlmodel import Session, create_engine

from app.models.user import User


load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL", "sqlite:///db.sqlite"))

def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session

def get_user_db(session: Session = Depends(get_session)) -> Generator[SQLModelUserDatabase, None, None]:
    yield SQLModelUserDatabase(session, User)
