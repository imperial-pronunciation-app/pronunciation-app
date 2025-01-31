
from sqlmodel import Session

from app.crud.generic_repository import GenericRepository
from app.models.recording import Recording


class RecordingRepository(GenericRepository[Recording]):

    def __init__(self, session: Session) -> None:
        super().__init__(session, Recording)
    
    def create(self, word_id: int, s3_key: str, user_id: int) -> Recording:
        recording = Recording(
            user_id=user_id,
            word_id=word_id,
            recording_s3_key=s3_key,
        )
        return self.add(recording)
