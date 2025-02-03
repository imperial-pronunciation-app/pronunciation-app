from fastapi_users_db_sqlmodel import SQLModelBaseUserDB

from app.models.id_model import IdModel


class User(IdModel, SQLModelBaseUserDB, table=True):
    pass
