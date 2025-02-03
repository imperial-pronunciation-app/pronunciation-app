
from typing import Sequence

from sqlmodel import Session, select

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
        return self.upsert(recording)
    
    def find_by_user(self, user_id: int) -> Sequence[Recording]:
        stmt = select(Recording).where(Recording.user_id == user_id)
        return self._session.exec(stmt).all()
    
    def find_by_word(self, word_id: int) -> Sequence[Recording]:
        stmt = select(Recording).where(Recording.word_id == word_id)
        return self._session.exec(stmt).all()
