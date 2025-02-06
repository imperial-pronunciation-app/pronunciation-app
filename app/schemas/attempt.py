from typing import List

from pydantic import BaseModel

from app.schemas.phoneme import PhonemePublic


class AttemptResponse(BaseModel):
    recording_id: int
    score: int
    recording_phonemes: List[PhonemePublic]
    xp_gain: int
