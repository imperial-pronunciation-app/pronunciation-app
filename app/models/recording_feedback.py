from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from .model_feedback import ModelFeedback
from .recording import Recording


class RecordingFeedback(SQLModel, table=True):
    recording_id: Optional[int] = Field(foreign_key="recording.id", primary_key=True)
    feedback: str
    score: int = Field(gt=-1, lt=101)

    recording: Optional["Recording"] = Relationship(back_populates="feedback")
    model_feedback: Optional["ModelFeedback"] = Relationship(back_populates="recording_feedback")
