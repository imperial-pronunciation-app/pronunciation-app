from typing import List, Optional, Tuple, TypeAlias

from app.schemas.phoneme import PhonemePublic


AlignedPhonemes: TypeAlias = List[Tuple[Optional[PhonemePublic], Optional[PhonemePublic]]]