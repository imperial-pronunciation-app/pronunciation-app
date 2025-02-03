from app.crud.unit_of_work import UnitOfWork
from app.models.user import User
from app.schemas.leaderboard import LeaderboardEntry, LeaderboardResponse
from app.utils.days import days_until_next_sunday


class LeaderboardService:

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    def get_global_leaderboard_for_user(self, user: User) -> LeaderboardResponse:
        leaderboard_user = self._uow.leaderboard_users.get_by_user(user.id)
        days_until_end = days_until_next_sunday()
        league = leaderboard_user.league

        leaders = self._uow.leaderboard_users.find_by_league_order_by_xp_desc_with_limit(league)
        leader_users = [self._uow.users.get_by_id(leader.user_id) for leader in leaders]
        leader_entries = [LeaderboardEntry(i + 1, leader_user[1].email, leader_user[0].xp) for i, leader_user in enumerate(zip(leaders, leader_users))]
        return LeaderboardResponse(
            league=league,
            days_until_end=days_until_end,
            leaders=leader_entries,
            current=[LeaderboardEntry(rank=0, username=user.email, xp=leaderboard_user.xp)] # Will add proper rank and users around the user in the future using redis
        )
    
    def reset_leaderboard(self) -> None:
        self._handle_promotions_and_demotions()
        self._set_zero()
        self._uow.commit()
    
    def _handle_promotions_and_demotions(self) -> None:
        """Handled by redis"""
        pass

    def _set_zero(self) -> None:
        records = self._uow.leaderboard_users.all()
        for record in records:
            record.xp = 0
        self._uow.leaderboard_users.upsert_all(records)
