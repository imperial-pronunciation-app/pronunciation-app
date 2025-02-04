from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship

from app.models.id_model import IdModel
from app.models.user import User


if TYPE_CHECKING:
    from app.models.attempt import Attempt
    from app.models.lesson import Lesson
    from app.models.word import Word

class Exercise(IdModel, table=True):
    lesson_id: int = Field(foreign_key="lesson.id")
    lesson: "Lesson" = Relationship(back_populates="exercises")
    index: int
    word_id: int = Field(foreign_key="word.id")
    word: "Word" = Relationship(back_populates="exercises")
    attempts: List["Attempt"] = Relationship(back_populates="exercise", cascade_delete=True)

    def get_previous_exercise(self) -> Optional["Exercise"]:
        """Returns the previous exercise within the lesson, or None if it's the first exercise."""
        sorted_exercises = sorted(self.lesson.exercises, key=lambda e: e.index)
        return sorted_exercises[self.index - 1] if self.index > 0 else None

    def get_next_exercise(self) -> Optional["Exercise"]:
        """Returns the next exercise within the lesson, or None if it's the last exercise."""
        sorted_exercises = sorted(self.lesson.exercises, key=lambda e: e.index)
        return sorted_exercises[self.index + 1] if self.index < len(sorted_exercises) - 1 else None
    
    def is_completed(self, user: User) -> bool:
        """Returns True if the user has completed this exercise. i.e. if exercise was attempted"""
        return any(attempt.user_id == user.id for attempt in self.attempts)