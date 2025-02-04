from datetime import datetime

from sqlmodel import Field

from app.models.id_model import IdModel


class Recording(IdModel, table=True):
    recording_s3_key: str
    attempt_id: int = Field(foreign_key="attempt.id")
    created_at: datetime = Field(default_factory=datetime.now)
