from typing import TYPE_CHECKING, List

from sqlmodel import Relationship

from app.models.id_model import IdModel


if TYPE_CHECKING:
    from app.models.lesson import Lesson


class Unit(IdModel, table=True):
    name: str
    description: str
    order: int
    lessons: List["Lesson"] = Relationship(back_populates="unit", cascade_delete=True)
