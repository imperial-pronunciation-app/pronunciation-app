from app.crud.unit_of_work import UnitOfWork
from app.models.recording import Recording


class RecordingService:

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow
    
    def create_recording(self, word_id: int, s3_key: str, user_id: int) -> Recording:
        recording = self._uow.recordings.create(word_id, s3_key, user_id)
        self._uow.commit()
        return recording
