from typing import List

from pydantic import BaseModel


class WordPhoneme(BaseModel):
    id: int
    ipa: str
    respelling: str


class RandomWord(BaseModel):
    word_id: int
    word: str
    word_phonemes: List[WordPhoneme]
