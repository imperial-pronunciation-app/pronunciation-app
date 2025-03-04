from typing import List

from pydantic import BaseModel


class InferWordPhonemesResponse(BaseModel):
    words: List[str]
    phonemes: List[str]
    success: bool