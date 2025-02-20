from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import Base


class IdModel(Base):
    """SQL Alchemy ORM class with an id field.
    """
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=None)
