from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, SQLModel


if TYPE_CHECKING:
    pass


# Possible words the user can pronounce
class Recording(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    recording_s3_key: str
    # user_id: int = Field(foreign_key="user.id")
    word_id: int = Field(foreign_key="word.id")
    time_created: datetime
