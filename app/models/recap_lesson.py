from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from app.models.lesson import Lesson

class RecapLesson(SQLModel, table=True):
    id: int = Field(primary_key=True, foreign_key="lesson.id")
    lesson: "Lesson" = Relationship(back_populates="recap_lesson")
    user_id: int = Field(primary_key=True, foreign_key="user.id")