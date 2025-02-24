from typing import TYPE_CHECKING, List

from sqlmodel import Relationship

from app.models.base.unit_base import UnitBase


if TYPE_CHECKING:
    from app.models.basic_lesson import BasicLesson


class Unit(UnitBase, table=True):
    order: int
    lessons: List["BasicLesson"] = Relationship(back_populates="unit", cascade_delete=True)
