from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.id_model import IdModel


class PhonemeBase(IdModel):
    __abstract__ = True

    ipa: Mapped[str] = mapped_column(String)
    respelling: Mapped[str] = mapped_column(String)