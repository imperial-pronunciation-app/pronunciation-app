from typing import List

from pydantic import BaseModel

from app.schemas.phoneme import PhonemePublic


class WordPublicWithPhonemes(BaseModel):
  id: int
  text: str
  phonemes: List[PhonemePublic]