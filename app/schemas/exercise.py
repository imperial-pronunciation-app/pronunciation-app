from pydantic import BaseModel

from app.schemas.word import WordPublicWithPhonemes


class ExerciseResponse(BaseModel):
    id: int
    word: WordPublicWithPhonemes
    is_completed: bool