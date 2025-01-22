from typing import List

from pydantic import BaseModel

from app.schemas.base import PhonemeSchema


class RandomWordResponse(BaseModel):
    word_id: int
    word: str
    word_phonemes: List[PhonemeSchema]