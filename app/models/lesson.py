from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.id_model import IdModel


if TYPE_CHECKING:
    from app.models.exercise import Exercise
    from app.models.unit import Unit

class Lesson(IdModel):
    __tablename__ = "lesson"

    unit_id: Mapped[int] = mapped_column(ForeignKey("unit.id"))
    unit: Mapped["Unit"] = relationship(back_populates="lessons")
    title: Mapped[str] = mapped_column(String)
    order: Mapped[int] = mapped_column(Integer)
    exercises: Mapped[List["Exercise"]] = relationship(back_populates="lesson", cascade="all, delete-orphan", order_by="Exercise.index")