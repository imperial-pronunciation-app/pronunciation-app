import os
import uuid

import requests
from fastapi import APIRouter, Depends, UploadFile

from app.config import get_settings
from app.crud.unit_of_work import UnitOfWork, get_unit_of_work
from app.models.user import User
from app.schemas.model_api import InferPhonemesResponse
from app.schemas.recording import RecordingRequest, RecordingResponse
from app.services.recording import RecordingService
from app.users import current_active_user
from app.utils.s3 import upload_wav_to_s3
from app.utils.similarity import similarity


router = APIRouter()

def create_wav_file(recording_request: RecordingRequest) -> str:
    temp_file = uuid.uuid4()
    filename = f"{temp_file}.wav"
    with open(filename, "bx") as f:
        f.write(recording_request.audio_bytes)
    return filename

def dispatch_to_model(wav_file: str) -> list[str]:
    with open(wav_file, "rb") as f:
        files = {
            "audio_file": f
        }

        print(get_settings().MODEL_API_URL)
        model_response = requests.post(f"{get_settings().MODEL_API_URL}/api/v1/infer_phonemes", files=files)

    model_response.raise_for_status()

    model_data = InferPhonemesResponse.model_validate(model_response.json())

    return model_data.phonemes

@router.post("/api/v1/words/{word_id}/recording", response_model=RecordingResponse)
async def post_recording(
    word_id: int,
    audio_file: UploadFile,
    uow: UnitOfWork = Depends(get_unit_of_work),
    user: User = Depends(current_active_user),
) -> RecordingResponse:
    audio_bytes = await audio_file.read()
    recording_request = RecordingRequest(audio_bytes=audio_bytes) # TODO: Clean this up

    # 1. Send .wav file to blob store
    wav_file = create_wav_file(recording_request)
    s3_key = upload_wav_to_s3(wav_file)
    
    # 2. Store Recording entry with recording_url from blob store
    service = RecordingService(uow)
    recording = service.create_recording(0, s3_key)
    
    # 3. Dispatch recording to ML backend
    inferred_phoneme_strings = dispatch_to_model(wav_file)
    inferred_phonemes = list(map(lambda x: uow.phonemes.get_phoneme_by_ipa(x), inferred_phoneme_strings))
    
    # 4. Form feedback based on model response
    word_phonemes = list(map(lambda x: x.ipa, uow.phonemes.find_phonemes_by_word(word_id)))
    feedback = similarity(word_phonemes, inferred_phoneme_strings)
    
    # 6. Delete temporary file
    os.remove(wav_file)
    
    # 7. Serve response to user
    return RecordingResponse(recording_id=recording.id, score=feedback, recording_phonemes=inferred_phonemes)

