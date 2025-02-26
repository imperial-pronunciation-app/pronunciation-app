from datetime import datetime

import pytest

from app.crud.analysis_repository import AnalyticsRepository
from app.models.analytics import EndpointAnalytics


@pytest.fixture
def sample_endpoint_analytics() -> None:
    AnalyticsRepository().upsert_analytics(
        EndpointAnalytics(
            endpoint="/api/v1/test", method="GET", status_code=200, duration=0.001122, timestamp=datetime.now()
        )
    )
