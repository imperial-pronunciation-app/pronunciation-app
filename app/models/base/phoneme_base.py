from app.models.id_model import IdModel


class PhonemeBase(IdModel):
    ipa: str
    respelling: str
    cdn_path: str
