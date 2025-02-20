from typing import TYPE_CHECKING, List

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base.unit_base import UnitBase


if TYPE_CHECKING:
    from app.models.lesson import Lesson

class Unit(UnitBase):
    __tablename__ = "unit"

    order: Mapped[int] = mapped_column(Integer)
    lessons: Mapped[List["Lesson"]] = relationship(back_populates="unit", cascade="all, delete-orphan")