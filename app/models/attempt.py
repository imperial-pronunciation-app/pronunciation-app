from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.id_model import IdModel


if TYPE_CHECKING:
    from app.models.exercise import Exercise

    
class Attempt(IdModel, table=True):
    exercise_id: int = Field(foreign_key="exercise.id")
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)
    exercise: "Exercise" = Relationship(back_populates="attempts")