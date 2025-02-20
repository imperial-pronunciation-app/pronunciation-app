from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.generic_repository import GenericRepository
from app.models.unit import Unit


class UnitRepository(GenericRepository[Unit]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Unit)
    
