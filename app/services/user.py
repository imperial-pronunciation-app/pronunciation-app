from app.crud.unit_of_work import UnitOfWork
from app.models.leaderboard_user import LeaderboardUser
from app.models.user import User


class UserService:

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow
    
    def update_xp(self, user: User, xp_gain: int) -> LeaderboardUser:
        assert xp_gain >= 0
        entry = user.leaderboard_user
        entry.xp += xp_gain
        entry = self._uow.leaderboard_users.upsert(entry)
        self._uow.commit()
        return entry
