from fastapi import APIRouter

from app.schemas.recording import Feedback, RecordingPhoneme, RecordingRequest

router = APIRouter()


@router.get("/api/v1/words/{word_id}/recording", response_model=Feedback)
async def get_random_word(recording_request: RecordingRequest):
    return Feedback(
        recording_id=recording_request.recording_id,
        score=1,
        recording_phonemes=[RecordingPhoneme(id=1, ipa="h", respelling="h")],
    )
