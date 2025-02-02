from typing import Optional

from sqlmodel import Session, select

from app.crud.generic_repository import GenericRepository
from app.models.user import User


class UserRepository(GenericRepository[User]):

    def __init__(self, session: Session):
        super().__init__(session, User)
    
    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        return self._session.exec(stmt).first()
