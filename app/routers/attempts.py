import os
import uuid

import requests
from fastapi import APIRouter, Depends, HTTPException, UploadFile

from app.config import get_settings
from app.crud.unit_of_work import UnitOfWork, get_unit_of_work
from app.models.attempt import Attempt
from app.models.recording import Recording
from app.models.user import User
from app.schemas.attempt import AttemptResponse
from app.schemas.model_api import InferPhonemesResponse
from app.services.pronunciation import PronunciationService
from app.services.unit import UnitService
from app.services.user import UserService
from app.users import current_active_user
from app.utils.s3 import upload_wav_to_s3


router = APIRouter()

def create_wav_file(audio_bytes: bytes) -> str:
    temp_file = uuid.uuid4()
    filename = f"{temp_file}.wav"
    with open(filename, "bx") as f:
        f.write(audio_bytes)
    return filename

def dispatch_to_model(wav_file: str) -> list[str]:
    with open(wav_file, "rb") as f:
        files = {
            "audio_file": f
        }

        print(get_settings().MODEL_API_URL)
        model_response = requests.post(f"{get_settings().MODEL_API_URL}/api/v1/eng/infer_phonemes", files=files)

    model_response.raise_for_status()

    model_data = InferPhonemesResponse.model_validate(model_response.json())

    return model_data.phonemes

@router.post("/api/v1/exercises/{exercise_id}/attempts", response_model=AttemptResponse)
async def post_attempt(
    exercise_id: int,
    audio_file: UploadFile,
    uow: UnitOfWork = Depends(get_unit_of_work),
    user: User = Depends(current_active_user),
) -> AttemptResponse:
    exercise = uow.exercises.find_by_id(exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    audio_bytes = await audio_file.read()

    # 1. Send .wav file to blob store
    wav_file = create_wav_file(audio_bytes)
    s3_key = upload_wav_to_s3(wav_file)
    
    # 2. Dispatch recording to ML backend
    inferred_phoneme_strings = dispatch_to_model(wav_file)
    
    # 3. Form feedback based on model response
    aligned_phonemes, score = PronunciationService(uow).evaluate_pronunciation(exercise.word, inferred_phoneme_strings)

    # 4. Create attempt and recording entries
    attempt = uow.attempts.upsert(
        Attempt(
            user_id=user.id,
            exercise_id=exercise_id,
            score=score
        )
    )

    recording = uow.recordings.upsert(
        Recording(
            attempt_id=attempt.id,
            s3_key=s3_key
        )
    )

    uow.commit()
    
    # 5. Update user xp based on feedback
    user_service = UserService(uow)
    xp_gain = user_service.update_xp_with_boost(user, score)

    # 6. Delete temporary file
    os.remove(wav_file)

    # 7. Generate recap lesson if this is the last exercise of the last lesson
    unit_service = UnitService(uow)
    if unit_service._is_completed_by(exercise.lesson.unit, user):
        print("Generating recap lesson")
        recap_lesson = unit_service.generate_recap_lesson(exercise.lesson.unit, user)
        uow.lessons.upsert(recap_lesson)
        uow.commit()
        
    # 8. Serve response to user
    return AttemptResponse(
        recording_id=recording.id,
        score=score,
        phonemes=aligned_phonemes,
        xp_gain=xp_gain
    )
