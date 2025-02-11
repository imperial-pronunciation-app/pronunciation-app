from fastapi import APIRouter, Depends

from app.crud.unit_of_work import UnitOfWork, get_unit_of_work
from app.models.user import User
from app.schemas.word_of_day import WordOfDayResponse
from app.services.word import WordService
from app.users import current_active_user


router = APIRouter()


@router.get("/api/v1/word_of_day", response_model=WordOfDayResponse)
async def get_word_of_day(
    uow: UnitOfWork = Depends(get_unit_of_work), user: User = Depends(current_active_user)
) -> WordOfDayResponse:
    today_word = uow.word_of_day.get_word_of_day()
    return WordOfDayResponse(
        word=WordService(uow).to_public_with_phonemes(today_word.word),
        id=today_word.word_id,
    )
