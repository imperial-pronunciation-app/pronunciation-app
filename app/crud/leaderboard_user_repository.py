from typing import Optional, Sequence

from sqlmodel import Session, desc, select

from app.crud.generic_repository import GenericRepository
from app.models.leaderboard_user import LeaderboardUser, League


class LeaderboardUserRepository(GenericRepository[LeaderboardUser]):

    def __init__(self, session: Session) -> None:
        super().__init__(session, LeaderboardUser)
    
    def find_by_league_order_by_xp_desc_with_limit(self, league: League, limit: int = 3) -> Sequence[LeaderboardUser]:
        stmt = (
            select(LeaderboardUser)
            .where(LeaderboardUser.league == league)
            .limit(limit)
            .order_by(desc(LeaderboardUser.xp))
        )
        return self._session.exec(stmt).all()
    
    def find_by_user(self, user_id: int) -> Optional[LeaderboardUser]:
        stmt = select(LeaderboardUser).where(LeaderboardUser.user_id == user_id)
        return self._session.exec(stmt).first()