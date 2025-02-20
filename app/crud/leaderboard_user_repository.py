from typing import Sequence

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.generic_repository import GenericRepository
from app.models.leaderboard_user_link import LeaderboardUserLink, League


class LeaderboardUserRepository(GenericRepository[LeaderboardUserLink]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, LeaderboardUserLink)
    
    async def find_by_league_order_by_xp_desc_with_limit(self, league: League, limit: int = 3) -> Sequence[LeaderboardUserLink]:
        stmt = (
            select(LeaderboardUserLink)
            .where(LeaderboardUserLink.league == league)
            .limit(limit)
            .order_by(desc(LeaderboardUserLink.xp))
        )
        return (await self._session.execute(stmt)).scalars().all()
    
    async def find_by_league(self, league: League) -> Sequence[LeaderboardUserLink]:
        stmt = (
            select(LeaderboardUserLink)
            .where(LeaderboardUserLink.league == league)
        )
        return (await self._session.execute(stmt)).scalars().all()
    
    async def get_by_user(self, user_id: int) -> LeaderboardUserLink:
        stmt = select(LeaderboardUserLink).where(LeaderboardUserLink.user_id == user_id)
        return (await self._session.execute(stmt)).scalar_one()
