from typing import List

from pydantic import BaseModel


class RecordingRequest(BaseModel):
    recording: bytes


class RecordingPhoneme(BaseModel):
    id: int
    ipa: str
    respelling: str


class Feedback(BaseModel):
    recording_id: int
    score: int
    recording_phonemes: List[RecordingPhoneme]
