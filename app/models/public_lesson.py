from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from app.models.lesson import Lesson

class PublicLesson(SQLModel, table=True):
    id: int = Field(primary_key=True, foreign_key="lesson.id")
    lesson: "Lesson" = Relationship(back_populates="recap_lesson")
    order: int