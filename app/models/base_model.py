from typing import Optional

from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    """Base SQL model class. Requires all tables to have an id field.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
