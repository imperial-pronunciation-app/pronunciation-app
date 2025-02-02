from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field

from app.models.id_model import IdModel


if TYPE_CHECKING:
    pass


# Possible words the user can pronounce
class Recording(IdModel, table=True):
    recording_s3_key: str
    user_id: int = Field(foreign_key="user.id")
    word_id: int = Field(foreign_key="word.id")
    created_at: datetime = Field(default_factory=datetime.now)
