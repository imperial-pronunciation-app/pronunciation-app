from app.models.id_model import IdModel


class LanguageBase(IdModel):
    code: str
    name: str
