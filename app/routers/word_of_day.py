from fastapi import APIRouter, Depends

from app.crud.unit_of_work import UnitOfWork, get_unit_of_work
from app.models.user import User
from app.schemas.word import WordPublicWithPhonemes
from app.services.word import WordService
from app.users import current_active_user


router = APIRouter()


@router.get("/api/v1/word_of_day", response_model=WordPublicWithPhonemes)
async def get_word_of_day(
    uow: UnitOfWork = Depends(get_unit_of_work),
    user: User = Depends(current_active_user)
) -> WordPublicWithPhonemes:
    today_word = uow.word_of_day.get_word_of_day(user.language_id)
    return WordService(uow).to_public_with_phonemes(today_word.word)
