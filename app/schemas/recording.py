from typing import List

from pydantic import BaseModel

from app.models.phoneme import Phoneme


class RecordingRequest(BaseModel):
    # user_id: int
    audio_bytes: bytes

class RecordingResponse(BaseModel):
    recording_id: int
    score: int
    recording_phonemes: List[Phoneme]

