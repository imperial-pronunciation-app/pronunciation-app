from pydantic import BaseModel

from app.schemas.word import WordPublicWithPhonemes


class WordOfDayResponse(BaseModel):
    word: WordPublicWithPhonemes
