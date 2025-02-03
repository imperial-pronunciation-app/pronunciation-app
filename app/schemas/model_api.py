from typing import List

from pydantic import BaseModel


class InferPhonemesResponse(BaseModel):
    phonemes: List[str]