from fastapi import APIRouter, Depends, HTTPException

from app.crud.unit_of_work import UnitOfWork, get_unit_of_work
from app.models.user import User
from app.schemas.word import WordPublicWithPhonemes
from app.services.word import WordService
from app.users import current_active_user


router = APIRouter()

@router.get("/api/v1/continuous_practice", response_model=WordPublicWithPhonemes)
async def get_continuous_practice_word(uow: UnitOfWork = Depends(get_unit_of_work), user: User = Depends(current_active_user)) -> WordPublicWithPhonemes:
  word_service = WordService(uow)

  try:
    return word_service.to_public_with_phonemes(word_service.get_random())
  except IndexError:
    raise HTTPException(503, "No words are available for practice.")
