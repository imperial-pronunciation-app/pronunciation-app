from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.id_model import IdModel


class WordBase(IdModel):
    __abstract__ = True
    
    text: Mapped[str] = mapped_column(String)