from typing import List, Optional, Tuple

from pydantic import BaseModel

from app.schemas.phoneme import PhonemePublic


class AttemptResponse(BaseModel):
    recording_id: int
    score: int
    phonemes: List[Tuple[Optional[PhonemePublic], Optional[PhonemePublic]]]
    xp_gain: int

class ExerciseAttemptResponse(AttemptResponse):
    exercise_is_completed: bool