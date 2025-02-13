from fastapi import APIRouter, Depends

from app.crud.unit_of_work import UnitOfWork, get_unit_of_work
from app.schemas.word import WordPublicWithPhonemes
from app.services.word import WordService


router = APIRouter()

@router.get("/api/v1/continuous_practice", response_model=WordPublicWithPhonemes)
async def get_continuous_practice_word(uow: UnitOfWork = Depends(get_unit_of_work)) -> WordPublicWithPhonemes:
  word_service = WordService(uow)

  return word_service.to_public_with_phonemes(word_service.get_random())
