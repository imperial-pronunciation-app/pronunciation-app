from app.models.id_model import IdModel


class PhonemeBase(IdModel):
    ipa: str
    cdn_path: str