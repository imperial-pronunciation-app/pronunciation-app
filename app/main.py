from typing import Dict

from fastapi import FastAPI
from sqladmin import Admin

from app.admin.auth import AdminAuth
from app.admin.user_admin import UserAdmin
from app.cron import lifespan
from app.database import engine
from app.routers import routers


app = FastAPI(lifespan=lifespan)
admin = Admin(app, engine, authentication_backend=AdminAuth())
admin.add_view(UserAdmin)


@app.get("/")
def read_home() -> Dict[str, str]:  # would be a Pydantic return type normally
    return {"Hello": "James"}


for router in routers:
    app.include_router(router)


if __name__ == "__main__":
    pass
