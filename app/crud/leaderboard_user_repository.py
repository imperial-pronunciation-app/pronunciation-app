from typing import Sequence

from sqlmodel import Session, desc, select

from app.crud.generic_repository import GenericRepository
from app.models.leaderboard_user_link import LeaderboardUserLink, League


class LeaderboardUserRepository(GenericRepository[LeaderboardUserLink]):

    def __init__(self, session: Session) -> None:
        super().__init__(session, LeaderboardUserLink)
    
    def find_by_league_order_by_xp_desc_with_limit(self, league: League, limit: int = 3) -> Sequence[LeaderboardUserLink]:
        stmt = (
            select(LeaderboardUserLink)
            .where(LeaderboardUserLink.league == league)
            .limit(limit)
            .order_by(desc(LeaderboardUserLink.xp))
        )
        return self._session.exec(stmt).all()
    
    def find_by_league(self, league: League) -> Sequence[LeaderboardUserLink]:
        stmt = (
            select(LeaderboardUserLink)
            .where(LeaderboardUserLink.league == league)
        )
        return self._session.exec(stmt).all()
    
    def get_by_user(self, user_id: int) -> LeaderboardUserLink:
        stmt = select(LeaderboardUserLink).where(LeaderboardUserLink.user_id == user_id)
        return self._session.exec(stmt).one()
