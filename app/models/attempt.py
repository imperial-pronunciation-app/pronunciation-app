from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.id_model import IdModel


if TYPE_CHECKING:
    from app.models.exercise import Exercise


class Attempt(IdModel):
    __tablename__ = "attempt"

    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercise.id"))
    exercise: Mapped["Exercise"] = relationship(back_populates="attempts")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)