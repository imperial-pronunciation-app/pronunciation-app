import os
from typing import Iterator

from dotenv import load_dotenv
from sqlmodel import Session, create_engine


load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL", "sqlite:///db.sqlite"))


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
