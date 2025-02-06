from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship

from app.models.id_model import IdModel
from app.models.unit import Unit


if TYPE_CHECKING:
    from app.models.exercise import Exercise

class Lesson(IdModel, table=True):
    unit_id: int = Field(foreign_key="unit.id")
    unit: Unit = Relationship(back_populates="lessons")
    title: str
    order: int
    exercises: List["Exercise"] = Relationship(back_populates="lesson", cascade_delete=True, sa_relationship_kwargs={"order_by": "Exercise.index"})
    
    def first_exercise(self) -> "Exercise":
        return self.exercises[0]