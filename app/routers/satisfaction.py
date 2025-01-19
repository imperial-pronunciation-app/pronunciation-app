from fastapi import APIRouter
from schemas.satisfaction import SatisfactionRequest

router = APIRouter()


@router.get("/api/v1/recordings/{recording_id}/satisfaction", status_code=204)
async def get_random_word(satisfaction_request: SatisfactionRequest):
    return None
