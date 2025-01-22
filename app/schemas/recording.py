from typing import List

from pydantic import BaseModel

from app.schemas.base import PhonemeSchema


class RecordingRequest(BaseModel):
    recording: bytes

class RecordingResponse(BaseModel):
    recording_id: int
    score: int
    recording_phonemes: List[PhonemeSchema]

