from app.crud.unit_of_work import UnitOfWork
from app.models.recording import Recording


class RecordingService:

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow
    
    def create_recording(self, attempt_id: int, s3_key: str) -> Recording:
        recording = self._uow.recordings.create(attempt_id, s3_key)
        self._uow.commit()
        return recording
