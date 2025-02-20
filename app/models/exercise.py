from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.id_model import IdModel


if TYPE_CHECKING:
    from app.models.attempt import Attempt
    from app.models.lesson import Lesson
    from app.models.word import Word

class Exercise(IdModel):
    __tablename__ = "exercise"

    lesson_id: Mapped[int] = mapped_column(ForeignKey("lesson.id"))
    lesson: Mapped["Lesson"] = relationship(back_populates="exercises")
    index: Mapped[int] = mapped_column(Integer)
    word_id: Mapped[int] = mapped_column(ForeignKey("word.id"))
    word: Mapped["Word"] = relationship(back_populates="exercises")
    attempts: Mapped[List["Attempt"]] = relationship(back_populates="exercise", cascade="all, delete-orphan")