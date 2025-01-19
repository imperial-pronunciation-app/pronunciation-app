from fastapi import APIRouter
from schemas.random_word import RandomWord, WordPhoneme

router = APIRouter()


@router.get("/api/v1/random_word", response_model=RandomWord)
async def get_random_word():
    return RandomWord(
        word_id=1,
        word="hello",
        word_phonemes=[
            WordPhoneme(id=1, ipa="h", respelling="h"),
            WordPhoneme(id=2, ipa="ɛ", respelling="e"),
            WordPhoneme(id=3, ipa="l", respelling="l"),
            WordPhoneme(id=4, ipa="oʊ", respelling="o"),
        ],
    )
