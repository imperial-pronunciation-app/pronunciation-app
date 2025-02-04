from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship

from app.models.id_model import IdModel
from app.models.unit import Unit
from app.models.user import User
from app.schemas.lesson import LessonResponse


if TYPE_CHECKING:
    from app.models.exercise import Exercise

class Lesson(IdModel, table=True):
    unit_id: int = Field(foreign_key="unit.id")
    unit: Unit = Relationship(back_populates="lessons")
    title: str
    order: int
    exercises: List["Exercise"] = Relationship(back_populates="lesson", cascade_delete=True)

    def to_response(self, user: User) -> LessonResponse:
        return LessonResponse(
            title=self.title,
            is_completed=self.is_completed(user),
            first_exercise_id=self.first_exercise().id
        )
    
    def is_completed(self, user: User) -> bool:
        return all(exercise.is_completed(user) for exercise in self.exercises)
    
    def first_exercise(self) -> "Exercise":
        return min(self.exercises, key=lambda e: e.index)