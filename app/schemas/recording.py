from pydantic import BaseModel


class SatisfactionRequest(BaseModel):
    satisfied: bool
