from datetime import datetime

from app.crud.analysis_repository import AnalyticsRepository
from app.crud.unit_of_work import UnitOfWork
from app.models.analytics import EndpointAnalytics


def test_create_endpoint_analytics(uow: UnitOfWork) -> None:
    """Test creating endpoint analytics entry"""
    analytics = EndpointAnalytics(
        endpoint="/api/v1/word_of_day", method="GET", status_code=401, duration=0.001122, timestamp=datetime.utcnow()
    )

    AnalyticsRepository().upsert_analytics(analytics)

    AnalyticsRepository().get_count_of_endpoint_and_response_time()


def test_get_analytics_data(uow: UnitOfWork, sample_endpoint_analytics: EndpointAnalytics) -> None:
    """Test retrieving analytics data"""
    results = AnalyticsRepository().get_count_of_endpoint_and_response_time()

    assert len(results) > 0
    assert any(r[0] == "/api/v1/test" for r in results)
