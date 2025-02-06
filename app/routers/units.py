from fastapi import APIRouter, Depends

from app.crud.unit_of_work import UnitOfWork, get_unit_of_work
from app.models.user import User
from app.schemas.unit import UnitsResponse
from app.services.unit import UnitService
from app.users import current_active_user


router = APIRouter()


@router.get("/api/v1/units", response_model=UnitsResponse)
async def get_units(uow: UnitOfWork = Depends(get_unit_of_work), user: User = Depends(current_active_user)) -> UnitsResponse:
    units = uow.units.all()
    unit_service = UnitService(uow)
    return UnitsResponse(
        units=[unit_service.to_public_with_lessons(unit, user) for unit in units]
    )
