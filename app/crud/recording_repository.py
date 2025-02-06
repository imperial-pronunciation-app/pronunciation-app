

from sqlmodel import Session

from app.crud.generic_repository import GenericRepository
from app.models.recording import Recording


class RecordingRepository(GenericRepository[Recording]):

    def __init__(self, session: Session) -> None:
        super().__init__(session, Recording)
    
