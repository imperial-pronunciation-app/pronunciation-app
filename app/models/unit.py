from typing import TYPE_CHECKING, List

from sqlmodel import Relationship

from app.models.base.unit_base import UnitBase


if TYPE_CHECKING:
    from app.models.lesson import Lesson


class Unit(UnitBase, table=True):
    order: int
    lessons: List["Lesson"] = Relationship(back_populates="unit", cascade_delete=True)
