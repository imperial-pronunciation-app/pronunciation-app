from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from .recording import Recording


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str
    recordings: List["Recording"] = Relationship(back_populates="user")
