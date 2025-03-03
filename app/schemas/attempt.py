from pydantic import BaseModel

from app.schemas.aligned_phonemes import AlignedPhonemes


class AttemptResponse(BaseModel):
    success: bool
    recording_id: int
    score: int
    phonemes: AlignedPhonemes
    xp_gain: int
