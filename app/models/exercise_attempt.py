from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.id_model import IdModel


if TYPE_CHECKING:
  from app.models.attempt import Attempt
  from app.models.exercise import Exercise

class ExerciseAttempt(IdModel, table=True):
  id: int = Field(primary_key=True, foreign_key="attempt.id")
  attempt: "Attempt" = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "ExerciseAttempt.id == Attempt.id",
            "lazy": "joined",
            "uselist": False
        }
    )
  exercise_id: int = Field(foreign_key="exercise.id")
  exercise: "Exercise" = Relationship(back_populates="attempts")
