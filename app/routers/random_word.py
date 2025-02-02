import random

from fastapi import APIRouter, Depends, HTTPException

from app.crud.unit_of_work import UnitOfWork, get_unit_of_work
from app.schemas.base import PhonemeSchema
from app.schemas.random_word import RandomWordResponse


router = APIRouter()


@router.get("/api/v1/random_word", response_model=RandomWordResponse)
async def get_random_word(uow: UnitOfWork = Depends(get_unit_of_work)) -> RandomWordResponse:
    words = uow.words.all()
    if not words:
        raise HTTPException(status_code=404, detail="No words found")

    random_word = random.choice(words)
    
    # Find phonemes for the random word
    phonemes = uow.phonemes.find_phonemes_by_word(random_word.id)

    word_phonemes = []
    for phoneme in phonemes:
        word_phonemes.append(PhonemeSchema(id=phoneme.id, ipa=phoneme.ipa, respelling=phoneme.respelling))

    return RandomWordResponse(word_id=random_word.id, word=random_word.word, word_phonemes=word_phonemes)
