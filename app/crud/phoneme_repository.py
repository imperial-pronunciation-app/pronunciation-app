from sqlmodel import Session, select

from app.models.phoneme import Phoneme


class PhonemeRepository:
    def __init__(self, session: Session) -> None:
        self.session = session
    
    def get_phoneme_by_ipa(self, ipa: str) -> Phoneme:
        print(ipa)
        phoneme = self.session.exec(select(Phoneme).where(Phoneme.ipa == ipa)).first()
        print(phoneme)
        assert phoneme is not None
        return phoneme