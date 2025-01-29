from typing import TYPE_CHECKING

from fastapi_users_db_sqlmodel import SQLModelBaseUserDB
from sqlmodel import SQLModel


if TYPE_CHECKING:
    pass

class User(SQLModelBaseUserDB, SQLModel, table=True):
    pass