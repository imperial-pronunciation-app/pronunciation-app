from typing import List

from pydantic import BaseModel

from app.models.phoneme import Phoneme


class AttemptResponse(BaseModel):
    recording_id: int
    score: int
    recording_phonemes: List[Phoneme]

