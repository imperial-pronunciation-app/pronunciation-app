from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.id_model import IdModel


if TYPE_CHECKING:
    from app.models.lesson import Lesson

class Exercise(IdModel, table=True):
    lesson_id: int = Field(foreign_key="lesson.id")
    lesson: "Lesson" = Relationship(back_populates="exercises")
    order: int
    word_id: int = Field(foreign_key="word.id")