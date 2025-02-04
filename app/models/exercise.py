from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship

from app.models.id_model import IdModel
from app.models.user import User


if TYPE_CHECKING:
    from app.models.attempt import Attempt
    from app.models.lesson import Lesson

class Exercise(IdModel, table=True):
    lesson_id: int = Field(foreign_key="lesson.id")
    lesson: "Lesson" = Relationship(back_populates="exercises")
    index: int
    word_id: int = Field(foreign_key="word.id")
    attempts: List["Attempt"] = Relationship(back_populates="exercise", cascade_delete=True)
    
    def is_completed(self, user: User) -> bool:
        """Returns True if the user has completed this exercise. i.e. if exercise was attempted"""
        return any(attempt.user_id == user.id for attempt in self.attempts)