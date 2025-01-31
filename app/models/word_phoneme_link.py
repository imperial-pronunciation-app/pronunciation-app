from typing import Optional

from sqlmodel import Field

from app.models.base_model import BaseModel


class WordPhonemeLink(BaseModel, table=True):
    word_id: Optional[int] = Field(foreign_key="word.id", primary_key=True)
    phoneme_id: Optional[int] = Field(foreign_key="phoneme.id", primary_key=True)
