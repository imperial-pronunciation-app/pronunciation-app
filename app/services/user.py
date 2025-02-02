from app.crud.unit_of_work import UnitOfWork
from app.models.leaderboard_user import LeaderboardUser


class UserService:

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow
    
    def update_xp(self, user_id: int, xp_gain: int) -> LeaderboardUser:
        assert xp_gain >= 0
        entry = self._uow.leaderboard_users.find_by_user(user_id)
        if entry:
            entry.xp += xp_gain
        else:
            entry = LeaderboardUser(user_id=user_id, xp=xp_gain)
        entry = self._uow.leaderboard_users.upsert(entry)
        self._uow.commit()
        return entry
