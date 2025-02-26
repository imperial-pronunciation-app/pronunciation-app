from typing import Dict

import rollbar
from fastapi import FastAPI
from rollbar.contrib.fastapi import add_to as rollbar_add_to
from sqladmin import Admin

from app.admin import views
from app.admin.auth import AdminAuth
from app.config import get_settings
from app.cron import lifespan
from app.database import engine
from app.routers import routers


rollbar.init(
    get_settings().ROLLBAR_ACCESS_TOKEN,
    environment=get_settings().ROLLBAR_ENVIRONMENT,
    handler="async",
    include_request_body=True,
)

app = FastAPI(lifespan=lifespan)
rollbar_add_to(app)

admin = Admin(app, engine, authentication_backend=AdminAuth())
for view in views:
    admin.add_view(view)


@app.get("/")
def read_home() -> Dict[str, str]:  # would be a Pydantic return type normally
    return {"Hello": "James"}


for router in routers:
    app.include_router(router)


if __name__ == "__main__":
    pass
