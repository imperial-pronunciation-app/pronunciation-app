import os
import uuid

import boto3


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