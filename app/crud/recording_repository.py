from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.generic_repository import GenericRepository
from app.models.recording import Recording


class RecordingRepository(GenericRepository[Recording]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Recording)
    
