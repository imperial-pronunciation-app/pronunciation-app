from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .recording_feedback import RecordingFeedback


class ModelFeedback(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    recording_feedback_id: Optional[int] = Field(foreign_key="recordingfeedback.id")
    was_accurate: bool

    recording_feedback: Optional["RecordingFeedback"] = Relationship(back_populates="model_feedback")
    # recording: Optional["Recording"] = Relationship(back_populates="model_feedback")
