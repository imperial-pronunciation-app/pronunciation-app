from typing import Any, Sequence, Tuple

from sqlalchemy.engine.row import Row
from sqlmodel import func, select

from app.database import engine
from app.models.analytics import EndpointAnalytics


class AnalyticsRepository:
    def get_count_of_endpoint_and_response_time(self) -> Sequence[Row[Tuple[Tuple[str, int, Any]]]]:
        with engine.connect() as conn:
            query = select(
                EndpointAnalytics.endpoint,
                func.count().label("count"),
                func.avg(EndpointAnalytics.duration).label("avg_response_time"),
            ).group_by(EndpointAnalytics.endpoint)

            results: Sequence[Row[Tuple[Tuple[str, int, Any]]]] = conn.execute(query).fetchall()
            return results
