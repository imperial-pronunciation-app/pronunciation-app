from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    display_name: str


class UserCreate(schemas.BaseUserCreate):
    display_name: str


class UserUpdate(schemas.BaseUserUpdate):
    display_name: Optional[str] = None
