import os
import uuid

import requests
from fastapi import APIRouter, Depends, UploadFile
from sqlmodel import Session, col, select

from app.config import get_settings
from app.crud.recording_repository import RecordingRepository
from app.database import get_session
from app.models.phoneme import Phoneme
from app.models.user import User
from app.models.word_phoneme_link import WordPhonemeLink
from app.schemas.model_api import InferPhonemesResponse
from app.schemas.recording import RecordingRequest, RecordingResponse
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
    files = {
        "audio_file": ("audio.wav", open(wav_file, "rb"), "audio/wav")
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
    session: Session = Depends(get_session),
    user: User = Depends(current_active_user)
) -> RecordingResponse:
    audio_bytes = await audio_file.read()
    recording_request = RecordingRequest(audio_bytes=audio_bytes) # TODO: Clean this up

    # 1. Send .wav file to blob store
    wav_file = create_wav_file(recording_request)
    s3_key = upload_wav_to_s3(wav_file)
    
    # # 2. Store Recording entry with recording_url from blob store
    recording_repository = RecordingRepository(session)
    recording = recording_repository.create(word_id, s3_key, user.id)
    
    # 3. Dispatch recording to ML backend
    inferred_phonemes = dispatch_to_model(wav_file)
    
    # 4. Form feedback based on model response
    phoneme_query = (
        select(Phoneme)
        .join(WordPhonemeLink)
        .where(WordPhonemeLink.word_id == word_id)
        .order_by(col(WordPhonemeLink.index))
        )
    phonemes = session.exec(phoneme_query).all()

    word_phonemes = []
    for phoneme in phonemes:
        assert phoneme.id is not None
        word_phonemes.append(phoneme.ipa)

    feedback = similarity(word_phonemes, inferred_phonemes)
    
    # 5. TODO: Store feedback in RecordingFeedback
    
    # 6. Delete temporary file
    os.remove(wav_file)
    
    # 7. Serve response to user
    assert recording.id is not None
    return RecordingResponse(recording_id=recording.id, score=feedback, recording_phonemes=[])

