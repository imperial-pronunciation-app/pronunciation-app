from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship

from app.models.id_model import IdModel


if TYPE_CHECKING:
    from app.models.exercise_attempt import ExerciseAttempt
    from app.models.lesson import Lesson
    from app.models.word import Word

class Exercise(IdModel, table=True):
    lesson_id: int = Field(foreign_key="lesson.id")
    lesson: "Lesson" = Relationship(back_populates="exercises")
    index: int
    word_id: int = Field(foreign_key="word.id")
    word: "Word" = Relationship(back_populates="exercises")
    attempts: List["ExerciseAttempt"] = Relationship(back_populates="exercise", cascade_delete=True)
