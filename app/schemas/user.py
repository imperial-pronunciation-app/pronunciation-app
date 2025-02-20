from datetime import date

from fastapi_users import schemas


class User(schemas.BaseUser[int]):
    login_streak: int
    last_login_date: date
    xp_total: int
    level: int
    new_user: bool
    created_at: date    

class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass