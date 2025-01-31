from typing import Optional, Sequence

from sqlmodel import Session, desc, select

from app.models.leaderboard_user import LeaderboardUser, League


class LeaderboardUserRepository:

    def __init__(self, session: Session) -> None:
        self.session = session
    
    def update_xp(self, user_id: int, league: League, xp_gain: int) -> LeaderboardUser:
        assert xp_gain >= 0
        statement = select(LeaderboardUser).where(LeaderboardUser.user_id == user_id, LeaderboardUser.league == league)
        entry = self.session.exec(statement).first()
        if entry:
            assert entry.league == league
            entry.xp += xp_gain
        else:
            entry = LeaderboardUser(user_id=user_id, league=league, xp=xp_gain)
            self.session.add(entry)
        self.session.commit()
        return entry
    
    def get_user_entry(self, user_id: int) -> Optional[LeaderboardUser]:
        statement = select(LeaderboardUser).where(LeaderboardUser.user_id == user_id)
        return self.session.exec(statement).first()
    
    def get_global_leaderboard(self, league: League) -> Sequence[LeaderboardUser]:
        TOP_K = 5
        statement = (
            select(LeaderboardUser)
            .where(LeaderboardUser.league == league)
            .order_by(desc(LeaderboardUser.xp))
            .limit(TOP_K)
        )
        result = self.session.exec(statement).all()
        return result
    
    def reset_leaderboard(self) -> None:
        self.session.commit()
