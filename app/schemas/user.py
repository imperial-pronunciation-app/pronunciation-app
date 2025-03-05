from typing import Optional

from fastapi_users import schemas


class UserCreate(schemas.BaseUserCreate):
    display_name: str


class UserUpdate(schemas.BaseUserUpdate):
    display_name: Optional[str] = None
    language_id: Optional[int] = None
