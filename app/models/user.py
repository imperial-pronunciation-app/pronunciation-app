from typing import TYPE_CHECKING

from fastapi_users_db_sqlmodel import SQLModelBaseUserDB


if TYPE_CHECKING:
    pass

class User(SQLModelBaseUserDB, table=True):
    pass