from pydantic import BaseModel


class PhonemePublic(BaseModel):
    id: int
    ipa: str
    respelling: str