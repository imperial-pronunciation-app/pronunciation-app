import uuid

import boto3

from app.config import get_settings


settings = get_settings()

def upload_wav_to_s3(wav_file: str) -> str:
    # TODO: Handle failure of uploading
    # TODO: Use async and await properly
    
    blob_id = uuid.uuid4()
    
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )
    
    s3_key = f"{blob_id}.wav"
    print(wav_file)
    s3_client.upload_file(wav_file, settings.BUCKET_NAME, s3_key)
  
    return s3_key