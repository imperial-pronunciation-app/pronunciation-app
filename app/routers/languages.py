from typing import List

from fastapi import APIRouter, Depends

from app.crud.unit_of_work import UnitOfWork, get_unit_of_work
from app.schemas.language import LanguagePublic
from app.services.language import LanguageService


router = APIRouter()


@router.get("/api/v1/languages", response_model=List[LanguagePublic])
async def get_languages(
    uow: UnitOfWork = Depends(get_unit_of_work)
) -> List[LanguagePublic]:
    language_service = LanguageService(uow)
    return language_service.to_public_sorted(uow.languages.all())
