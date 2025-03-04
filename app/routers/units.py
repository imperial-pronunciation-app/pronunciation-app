from fastapi import APIRouter, Depends, HTTPException

from app.crud.unit_of_work import UnitOfWork, get_unit_of_work
from app.models.user import User
from app.schemas.unit import UnitsResponse
from app.services.unit import UnitService
from app.users import current_active_user


router = APIRouter()


@router.get("/api/v1/{lang}/units", response_model=UnitsResponse)
async def get_units(lang: str, uow: UnitOfWork = Depends(get_unit_of_work), user: User = Depends(current_active_user)) -> UnitsResponse:
    language = uow.languages.get_by_name(lang)
    if not language:
        raise HTTPException(status_code=404, detail="Invalid language")
    units = uow.units.for_language(language.id)
    unit_service = UnitService(uow)
    return UnitsResponse(
        units=[unit_service.to_public_with_lessons(unit, user) for unit in units]
    )
