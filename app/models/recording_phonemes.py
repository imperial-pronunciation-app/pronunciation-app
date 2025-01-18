from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from .phoneme import Phoneme
from .recording import Recording


class RecordingPhonemes(SQLModel, table=True):
    recording_id: Optional[int] = Field(foreign_key="recording.id", primary_key=True)
    phoneme_id: Optional[int] = Field(foreign_key="phoneme.id", primary_key=True)
    index: int

    recording: Optional["Recording"] = Relationship(back_populates="phonemes")
    phoneme: Optional["Phoneme"] = Relationship(back_populates="recordings")
