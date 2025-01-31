import random

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, col, select

from app.database import get_session
from app.models import Phoneme, Word, WordPhonemeLink
from app.schemas.base import PhonemeSchema
from app.schemas.random_word import RandomWordResponse


router = APIRouter()


@router.get("/api/v1/random_word", response_model=RandomWordResponse)
async def get_random_word(session: Session = Depends(get_session)) -> RandomWordResponse:
    query = select(Word)
    words = session.exec(query).all()
    if not words:
        raise HTTPException(status_code=404, detail="No words found")

    random_word = random.choice(words)
    
    # Find phonemes for the random word
    phoneme_query = (
        select(Phoneme)
        .join(WordPhonemeLink)
        .where(WordPhonemeLink.word_id == random_word.id)
        .order_by(col(WordPhonemeLink.id))
        )
    phonemes = session.exec(phoneme_query).all()

    word_phonemes = []
    for phoneme in phonemes:
        assert phoneme.id is not None
        word_phonemes.append(PhonemeSchema(id=phoneme.id, ipa=phoneme.ipa, respelling=phoneme.respelling))

    assert random_word.id is not None
    return RandomWordResponse(word_id=random_word.id, word=random_word.word, word_phonemes=word_phonemes)
