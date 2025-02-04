

from sqlmodel import Session

from app.crud.generic_repository import GenericRepository
from app.models.recording import Recording


class RecordingRepository(GenericRepository[Recording]):

    def __init__(self, session: Session) -> None:
        super().__init__(session, Recording)
    
    def create(self, attempt_id: int, s3_key: str) -> Recording:
        recording = Recording(
            attempt_id=attempt_id,
            recording_s3_key=s3_key,
        )
        return self.upsert(recording)
    
