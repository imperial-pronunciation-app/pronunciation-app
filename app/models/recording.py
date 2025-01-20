from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .recording_feedback import RecordingFeedback
    from .user import User


class Recording(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    word_id: int = Field(foreign_key="word.id")
    time_created: datetime = Field(default_factory=datetime.utcnow)
    recording_url: str

    user: "User" = Relationship(back_populates="recordings")
    # word: "Word" = Relationship(back_populates="recordings")
    feedback: "RecordingFeedback" = Relationship(back_populates="recording")
