from typing import TYPE_CHECKING

from fastapi_users_db_sqlmodel import SQLModelBaseUserDB
from sqlmodel import Field, SQLModel


if TYPE_CHECKING:
    pass

class User(SQLModelBaseUserDB, SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)