from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field

from app.models.id_model import IdModel


if TYPE_CHECKING:
    pass


class Attempt(IdModel, table=True):
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)
