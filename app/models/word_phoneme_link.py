from typing import Optional
from sqlmodel import Field, SQLModel

class WordPhonemeLink(SQLModel, table = True):
    word_id: Optional[int] = Field(foreign_key="word.id", primary_key=True)
    phoneme_id: Optional[int] = Field(foreign_key="phoneme.id", primary_key=True)
    index: int