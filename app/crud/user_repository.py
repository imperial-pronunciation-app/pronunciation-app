from datetime import date
from typing import Sequence

from sqlmodel import Date, Session, cast, select

from app.crud.generic_repository import GenericRepository
from app.models.user import User


class UserRepository(GenericRepository[User]):

    def __init__(self, session: Session):
        super().__init__(session, User)
    
    def get_by_email(self, email: str) -> User:
        stmt = select(User).where(User.email == email)
        return self._session.exec(stmt).one()

    def find_by_new_users_created_before(self, created_before: date) -> Sequence[User]:
        stmt = select(User).where(User.new_user).where(cast(User.created_at, Date) < created_before)
        return self._session.exec(stmt).all()
