from datetime import date
from typing import Optional, Sequence
from uuid import UUID

from sqlmodel import Session, desc, select

from app.models.leaderboard import Leaderboard, League


class LeaderboardRepository:

    def __init__(self, session: Session) -> None:
        self.session = session
    
    def update_xp(self, user_id: UUID, league: League, xp_gain: int) -> Leaderboard:
        assert xp_gain >= 0
        statement = select(Leaderboard).where(Leaderboard.user_id == user_id, Leaderboard.league == league, Leaderboard.current)
        entry = self.session.exec(statement).first()
        if entry:
            assert entry.league == league
            entry.xp += xp_gain
        else:
            entry = Leaderboard(user_id=user_id, league=league, xp=xp_gain)
            self.session.add(entry)
        self.session.commit()
        return entry
    
    def get_user_current_entry(self, user_id: UUID) -> Optional[Leaderboard]:
        statement = select(Leaderboard).where(Leaderboard.user_id == user_id, Leaderboard.current)
        return self.session.exec(statement).first()
    
    def get_current_leaderboard(self, league: League) -> Sequence[Leaderboard]:
        TOP_K = 5
        statement = (
            select(Leaderboard)
            .where(Leaderboard.league == league, Leaderboard.current)
            .order_by(desc(Leaderboard.xp))
            .limit(TOP_K)
        )
        result = self.session.exec(statement).all()
        return result
    
    def reset_leaderboard(self) -> None:
        today = date.today()
        statement = select(Leaderboard).where(Leaderboard.current)
        result = self.session.exec(statement).all()
        for entry in result:
            entry.current = False
            entry.week_end = today
        self.session.commit()
