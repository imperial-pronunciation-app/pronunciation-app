from sqlmodel import Session
from datetime import datetime

from app.models.recording import Recording

class RecordingRepository:

    def __init__(self, session: Session) -> None:
        self.session = session
    
    def create(self, word_id: int, s3_key: str) -> bool:
        recording = Recording(
            # user_id=recording_request.user_id,
            word_id=word_id,
            recording_s3_key=s3_key,
            time_created=datetime.now()
        )
        self.session.add(recording)
        self.session.commit()

# recording_repository = RecordingRepository()