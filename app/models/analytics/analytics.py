from datetime import datetime

from app.models.analytics.http_method import HTTPMethod
from app.models.id_model import IdModel


class EndpointAnalytics(IdModel, table=True):
    endpoint: str
    method: HTTPMethod
    status_code: int
    duration: float
    timestamp: datetime
