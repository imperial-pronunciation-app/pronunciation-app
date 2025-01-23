from sqlmodel import Session

from app.models.recording import Recording


class RecordingRepository:

    def __init__(self, session: Session) -> None:
        self.session = session
    
    def create(self, recording: Recording) -> None:
        self.session.add(recording)
        self.session.commit()

# recording_repository = RecordingRepository()