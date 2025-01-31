import os
import string
import uuid
from typing import Dict

import dotenv
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlmodel import Session
from transformers.pipelines import Pipeline

from app.crud.recording_repository import RecordingRepository
from app.database import get_session
from app.models.user import User
from app.models.word import Word
from app.schemas.recording import RecordingRequest, RecordingResponse
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
    session: Session = Depends(get_session),
    user: User = Depends(current_active_user)
) -> RecordingResponse:
    audio_bytes = await audio_file.read()
    recording_request = RecordingRequest(audio_bytes=audio_bytes) # TODO: Clean this up

    # 1. Send .wav file to blob store
    wav_file = create_wav_file(recording_request)
    s3_key = upload_wav_to_s3(wav_file)
    
    # # 2. Store Recording entry with recording_url from blob store
    assert user.id
    recording_repository = RecordingRepository(session)
    recording = recording_repository.create(word_id, s3_key, user.id)
    
    # 3. Dispatch recording to ML backend
    model_response = dispatch_to_model(wav_file)
    
    # 4. Form feedback based on model response
    word = session.get(Word, word_id)
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    print(word)
    feedback = similarity(word.word, model_response)
    
    # 5. TODO: Store feedback in RecordingFeedback
    
    # 6. Delete temporary file
    os.remove(wav_file)
    
    # 7. Serve response to user
    assert recording.id is not None
    return RecordingResponse(recording_id=recording.id, score=feedback, recording_phonemes=[])

