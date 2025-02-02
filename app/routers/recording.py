import os
import string
import uuid
from typing import Dict

import dotenv
from fastapi import APIRouter, Depends, UploadFile
from transformers.pipelines import Pipeline

from app.crud.unit_of_work import UnitOfWork, get_unit_of_work
from app.models.user import User
from app.schemas.recording import RecordingRequest, RecordingResponse
from app.services.recording import RecordingService
from app.users import current_active_user
from app.utils.s3 import upload_wav_to_s3
from app.utils.similarity import similarity


dotenv.load_dotenv()

router = APIRouter()

ml_models: Dict[str, Pipeline] = {}

def create_wav_file(recording_request: RecordingRequest) -> str:
    temp_file = uuid.uuid4()
    filename = f"{temp_file}.wav"
    with open(filename, "bx") as f:
        f.write(recording_request.audio_bytes)
    return filename

def dispatch_to_model(wav_file: str) -> str:
    # TODO: Future models will return a list of phonemes
    model = ml_models["whisper"]
    return (
        str(model(wav_file)["text"])
        .lower()
        .strip()
        .translate(str.maketrans("", "", string.punctuation)) # Remove punctuation
    )

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
    
    # # 2. Store Recording entry with recording_url from blob store
    service = RecordingService(uow)
    recording = service.create_recording(word_id, s3_key, user.id)
    
    # 3. Dispatch recording to ML backend
    model_response = dispatch_to_model(wav_file)
    
    # 4. Form feedback based on model response
    word = uow.words.get_by_id(word_id)
    feedback = similarity(word.word, model_response)
    
    # 5. TODO: Store feedback in RecordingFeedback
    
    # 6. Delete temporary file
    os.remove(wav_file)
    
    # 7. Serve response to user
    return RecordingResponse(recording_id=recording.id, score=feedback, recording_phonemes=[])

