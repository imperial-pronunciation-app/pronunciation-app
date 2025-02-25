from typing import TYPE_CHECKING, List

from sqlmodel import Relationship

from app.models.id_model import IdModel


if TYPE_CHECKING:
    from app.models.exercise import Exercise

class Lesson(IdModel, table=True):
    title: str
    exercises: List["Exercise"] = Relationship(back_populates="lesson", cascade_delete=True, sa_relationship_kwargs={"order_by": "Exercise.index"})
