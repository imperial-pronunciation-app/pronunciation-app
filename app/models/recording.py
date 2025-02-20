from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.id_model import IdModel


class Recording(IdModel):
    __tablename__ = "recording"

    s3_key: Mapped[str] = mapped_column(String)
    attempt_id: Mapped[int] = mapped_column(ForeignKey("attempt.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)