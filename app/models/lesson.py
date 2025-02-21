from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship

from app.models.id_model import IdModel


if TYPE_CHECKING:
    from app.models.exercise import Exercise
    from app.models.unit import Unit

class Lesson(IdModel, table=True):
    unit_id: int = Field(foreign_key="unit.id")
    unit: "Unit" = Relationship(back_populates="lessons")
    order: Optional[int]
    title: str
    exercises: List["Exercise"] = Relationship(back_populates="lesson", cascade_delete=True, sa_relationship_kwargs={"order_by": "Exercise.index"})
    user_id: Optional[int] = Field(foreign_key="user.id")
