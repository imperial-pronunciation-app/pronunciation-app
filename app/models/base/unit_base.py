from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.id_model import IdModel


class UnitBase(IdModel):
    __abstract__ = True
    
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)