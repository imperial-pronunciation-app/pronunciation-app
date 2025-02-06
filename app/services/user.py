from app.crud.unit_of_work import UnitOfWork
from app.models.leaderboard_user_link import LeaderboardUserLink
from app.models.user import User
from app.redis import LRedis


class UserService:

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow
    
    def update_xp(self, user: User, xp_gain: int) -> LeaderboardUserLink:
        assert xp_gain >= 0
        entry = user.leaderboard_entry
        entry.xp += xp_gain
        entry = self._uow.leaderboard_users.upsert(entry)
        self._uow.commit()
        LRedis.update_xp(entry.league, entry.id, xp_gain)
        return entry
