from typing import List, Tuple

from fastapi import Request
from fastapi.responses import HTMLResponse
from sqladmin import BaseView, expose
from sqlmodel import func, select

from app.database import engine
from app.models.analytics import EndpointAnalytics


class AnalyticsDashboard(BaseView):
    name = "API Analytics"
    icon = "fa fa-chart-bar"

    @expose("/analytics", methods=["GET"])
    async def analytics(self, request: Request) -> HTMLResponse:
        with engine.connect() as conn:
            query = select(
                EndpointAnalytics.endpoint,
                func.count().label("count"),
                func.avg(EndpointAnalytics.duration).label("avg_response_time"),
            ).group_by(EndpointAnalytics.endpoint)

            results = conn.execute(query).fetchall()

            endpoints: List[str] = [str(r[0]) for r in results]
            counts: List[int] = [int(r[1]) for r in results]
            avg_times: List[float] = [round(float(r[2]), 2) if r[2] is not None else 0.0 for r in results]

            results_filtered: List[Tuple[str, int, float]] = [
                (endpoint, count, avg_time)
                for endpoint, count, avg_time in zip(endpoints, counts, avg_times)
                if "admin" not in endpoint
            ]

            if results_filtered:
                endpoints, counts, avg_times = map(list, zip(*results_filtered))
            else:
                endpoints, counts, avg_times = [], [], []

            chart_data = {
                "labels": endpoints,
                "datasets": [
                    {
                        "label": "Number of Calls",
                        "data": counts,
                        "backgroundColor": "rgba(75, 192, 192, 0.5)",
                        "borderColor": "rgb(75, 192, 192)",
                        "borderWidth": 1,
                    },
                    {
                        "label": "Avg Response Time (ms)",
                        "data": avg_times,
                        "backgroundColor": "rgba(255, 99, 132, 0.5)",
                        "borderColor": "rgb(255, 99, 132)",
                        "borderWidth": 1,
                        "yAxisID": "response-time",
                    },
                ],
            }
            return await self.templates.TemplateResponse(
                request, "admin/analytics.jinja2", context={"chart_data": chart_data}
            )
