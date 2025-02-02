from typing import TYPE_CHECKING

from fastapi_users_db_sqlmodel import SQLModelBaseUserDB

from app.models.id_model import IdModel


if TYPE_CHECKING:
    pass

class User(IdModel, SQLModelBaseUserDB, table=True):
    pass
