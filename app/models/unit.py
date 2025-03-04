from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship

from app.models.base.unit_base import UnitBase


if TYPE_CHECKING:
    from app.models.basic_lesson import BasicLesson
    from app.models.language import Language

class Unit(UnitBase, table=True):
    index: int
    lessons: List["BasicLesson"] = Relationship(back_populates="unit", cascade_delete=True)
    language_id: int = Field(foreign_key="language.id")
    language: "Language" = Relationship(back_populates="units")
