from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.id_model import IdModel


if TYPE_CHECKING:
  from app.models.unit import Unit


class BasicLesson(IdModel, table=True):
    id: int = Field(primary_key=True, foreign_key="lesson.id")
    order: int
    # TODO: Discuss, should this be on Lesson instead?
    # A Unit only needs to know about its basic lessons,
    # so that's the relationship
    unit_id: int = Field(foreign_key="unit.id")
    unit: "Unit" = Relationship(back_populates="lessons")