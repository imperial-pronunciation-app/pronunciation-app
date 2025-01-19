import random

from fastapi import APIRouter, Depends, HTTPException
from schemas.random_word import RandomWord, WordPhoneme
from sqlmodel import Session

from app.database import get_db
from app.models import Phoneme, Word, WordPhonemes

router = APIRouter()


@router.get("/api/v1/random_word", response_model=RandomWord)
async def get_random_word(db: Session = Depends(get_db)):
    words = db.exec(Word).all()
    if not words:
        raise HTTPException(status_code=404, detail="No words found")

    random_word = random.choice(words)

    # TODO: This can definitely be simplified
    word_phoneme_entries = (
        db.exec(WordPhonemes).filter(WordPhonemes.word_id == random_word.id).order_by(WordPhonemes.index).all()
    )
    phoneme_ids = [entry.phoneme_id for entry in word_phoneme_entries]
    word_phonemes = db.exec(Phoneme).filter(Phoneme.id.in_(phoneme_ids)).all()
    word_phonemes = [
        WordPhoneme(phoneme_id=phoneme.id, ipa=phoneme.ipa, respelling=phoneme.respelling) for phoneme in word_phonemes
    ]

    return RandomWord(word_id=random_word.id, word=random_word.word, word_phonemes=word_phonemes)
