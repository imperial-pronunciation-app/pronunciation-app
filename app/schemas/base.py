from pydantic import BaseModel


class PhonemeSchema(BaseModel):
    id: int
    ipa: str
    respelling: str
