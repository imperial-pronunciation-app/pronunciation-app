import os
from typing import Iterator

from app.models.user import User
from dotenv import load_dotenv
from sqlmodel import Session, create_engine
from fastapi import Depends
from fastapi_users_db_sqlmodel import SQLModelUserDatabase


load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL", "sqlite:///db.sqlite"))

def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session

def get_user_db(session: Session = Depends(get_session)):
    yield SQLModelUserDatabase(session, User)
