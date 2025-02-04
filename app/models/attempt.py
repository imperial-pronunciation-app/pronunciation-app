from datetime import datetime

from sqlmodel import Field

from app.models.id_model import IdModel


class Attempt(IdModel, table=True):
    exercise_id: int = Field(foreign_key="exercise.id")
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)