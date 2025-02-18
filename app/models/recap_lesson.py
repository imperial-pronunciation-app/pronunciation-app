from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.base.lesson_base import LessonBase


if TYPE_CHECKING:
    from app.models.user import User


class RecapLesson(LessonBase):
    user_id: int = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="recap_lessons")
    
    __mapper_args__ = {
        "polymorphic_identity": "recap_lesson",
    }