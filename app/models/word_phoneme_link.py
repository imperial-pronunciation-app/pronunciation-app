from typing import Optional

from sqlmodel import Field

from app.models.id_model import IdModel


class WordPhonemeLink(IdModel, table=True):
    word_id: Optional[int] = Field(foreign_key="word.id", primary_key=True)
    phoneme_id: Optional[int] = Field(foreign_key="phoneme.id", primary_key=True)
