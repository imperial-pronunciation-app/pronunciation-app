from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from .recording_feedback import RecordingFeedback


class ModelFeedback(SQLModel, table=True):
    recording_feedback_id: Optional[int] = Field(foreign_key="recording_feedback.id", primary_key=True)
    was_accurate: bool

    recording_feedback: Optional["RecordingFeedback"] = Relationship(back_populates="feedback")
