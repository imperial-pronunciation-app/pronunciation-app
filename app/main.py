from typing import Dict

from fastapi import FastAPI
from sqladmin import Admin

from app.admin import views
from app.admin.auth import AdminAuth
from app.cron import lifespan
from app.database import engine
from app.routers import routers


app = FastAPI(lifespan=lifespan)
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
