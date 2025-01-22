import os
import string
import uuid
from datetime import datetime

import boto3
import dotenv
from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.main import ml_models
from app.models.recording import Recording
from app.models.word import Word
from app.schemas.recording import RecordingRequest, RecordingResponse
from app.utils.similarity import similarity


dotenv.load_dotenv()

router = APIRouter()

def create_wav_file(recording_request: RecordingRequest) -> str:
    filename = f"{recording_request.user_id}.wav"
    with open(filename, "bx") as f:
      f.write(recording_request.audio_bytes)
    return filename

def upload_wav_to_s3(wav_file: str) -> str:
    # TODO: Handle failure of uploading
    # TODO: Use async and await properly
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION")
    bucket_name = os.getenv("BUCKET_NAME")
    
    blob_id = uuid.uuid4()
    
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )
    
    s3_key = f"{blob_id}.wav"
    s3_client.upload_file(wav_file, bucket_name, s3_key)
  
    return s3_key

def dispatch_to_model(wav_file: str) -> str:
    # TODO: Future models will return a list of phonemes
    model = ml_models["whisper"]
    return (
        str(model(wav_file)["text"])
        .lower()
        .strip()
        .translate(str.maketrans("", "", string.punctuation)) # Remove punctuation
    )

def form_feedback(model_response: str, word_id: int, session: Session) -> int:
    word = session.get(Word, word_id)
    if not word:
        return 0
    return similarity(word.word, model_response)

@router.post("/api/v1/words/{word_id}/recording", response_model=RecordingResponse)
async def post_recording(word_id: int, recording_request: RecordingRequest, session: Session = Depends(get_session)) -> RecordingResponse:
    
    # 1. Send .wav file to blob store
    wav_file = create_wav_file(recording_request)
    s3_key = upload_wav_to_s3(wav_file)
    
    # 2. Store Recording entry with recording_url from blob store
    # TODO: Move to CRUD
    recording = Recording(
        user_id=recording_request.user_id,
        word_id=word_id,
        recording_url=s3_key,
        time_created=datetime.now()
    )
    session.add(recording)
    session.commit()
    
    # 3. Dispatch recording to ML backend
    model_response = dispatch_to_model(wav_file)
    
    # 4. Form feedback based on model response
    feedback = form_feedback(model_response, word_id, session)
    
    # 5. TODO: Store feedback in RecordingFeedback
    
    # 6. Serve response to user
    assert recording.id is not None
    return RecordingResponse(recording_id=recording.id, score=feedback, recording_phonemes=[])

