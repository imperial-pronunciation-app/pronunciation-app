from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .model_feedback import ModelFeedback
    from .recording import Recording


class RecordingFeedback(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    recording_id: Optional[int] = Field(foreign_key="recording.id")
    feedback: str
    score: int = Field(gt=-1, lt=101)

    recording: Optional["Recording"] = Relationship(back_populates="feedback")
    model_feedback: Optional["ModelFeedback"] = Relationship(back_populates="recording_feedback")
