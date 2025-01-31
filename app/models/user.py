from typing import TYPE_CHECKING

from fastapi_users_db_sqlmodel import SQLModelBaseUserDB

from app.models.base_model import BaseModel


if TYPE_CHECKING:
    pass

class User(BaseModel, SQLModelBaseUserDB, table=True):
    pass
