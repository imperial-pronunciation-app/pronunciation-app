from typing import Optional

from sqlmodel import Field, SQLModel


class Word(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    word: str

    # phonemes: List["Phoneme"] = Relationship(back_populates="words")
