import os
import uuid

import requests
from fastapi import Depends, HTTPException, UploadFile

from app.config import get_settings
from app.crud.unit_of_work import UnitOfWork, get_unit_of_work
from app.models.attempt import Attempt
from app.models.exercise_attempt import ExerciseAttempt
from app.models.recording import Recording
from app.models.user import User
from app.models.word_of_day_attempt import WordOfDayAttempt
from app.schemas.attempt import AttemptResponse
from app.schemas.model_api import InferPhonemesResponse
from app.services.phoneme import PhonemeService
from app.services.user import UserService
from app.users import current_active_user
from app.utils.s3 import upload_wav_to_s3
from app.utils.similarity import similarity


class AttemptService:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def create_wav_file(self, audio_bytes: bytes) -> str:
        temp_file = uuid.uuid4()
        filename = f"{temp_file}.wav"
        with open(filename, "bx") as f:
            f.write(audio_bytes)
        return filename

    def dispatch_to_model(self, wav_file: str) -> list[str]:
        with open(wav_file, "rb") as f:
            files = {"audio_file": f}

            print(get_settings().MODEL_API_URL)
            model_response = requests.post(f"{get_settings().MODEL_API_URL}/api/v1/infer_phonemes", files=files)

        model_response.raise_for_status()

        model_data = InferPhonemesResponse.model_validate(model_response.json())

        return model_data.phonemes
    
    def get_attempt_feedback(self, wav_file: str, uow: UnitOfWork, user: User, word_id: int, recording_id: int) -> AttemptResponse:
        # 3. Dispatch recording to ML backend
        inferred_phoneme_strings = self.dispatch_to_model(wav_file)
        phoneme_service = PhonemeService(uow)
        inferred_phonemes = phoneme_service.get_public_phonemes(inferred_phoneme_strings)

        # 4. Form feedback based on model response

        word_phonemes = list(map(lambda x: x.ipa, uow.phonemes.find_phonemes_by_word(word_id)))
        feedback = similarity(word_phonemes, inferred_phoneme_strings)

        # 5. Update user xp based on feedback
        user_service = UserService(uow)
        xp_gain = user_service.update_xp_with_boost(user, feedback)

        # 6. Delete temporary file
        os.remove(wav_file)

        # 7. Serve response to user
        return AttemptResponse(
            recording_id=recording_id, score=feedback, recording_phonemes=inferred_phonemes, xp_gain=xp_gain
        )

    async def post_exercise_attempt(
        self,
        audio_file: UploadFile,
        exercise_id: int,
        uow: UnitOfWork = Depends(get_unit_of_work),
        user: User = Depends(current_active_user)
        ) -> AttemptResponse:
        exercise = uow.exercises.find_by_id(id=exercise_id)
        if not exercise:
            raise HTTPException(status_code=404, detail="Exercise not found")
        word_id = exercise.word.id
        
        audio_bytes = await audio_file.read()

        # 1. Send .wav file to blob store
        wav_file = self.create_wav_file(audio_bytes)
        s3_key = upload_wav_to_s3(wav_file)
        
        # 2. Create exercise attempt entries and recording entries
        attempt = uow.attempts.upsert(Attempt(user_id=user.id))
        uow.exercise_attempts.upsert(ExerciseAttempt(id=attempt.id, user_id=user.id, exercise_id=exercise_id))
        recording = uow.recordings.upsert(Recording(attempt_id=attempt.id, s3_key=s3_key))
        uow.commit()
        
        return self.get_attempt_feedback(wav_file, uow, user, word_id, recording.id)

    async def post_word_of_day_attempt(
        self,
        audio_file: UploadFile,
        word_of_day_id: int,
        uow: UnitOfWork = Depends(get_unit_of_work),
        user: User = Depends(current_active_user)
        ) -> AttemptResponse:
        word_of_day = uow.word_of_day.find_by_id(id=word_of_day_id)
        if not word_of_day:
            raise HTTPException(status_code=404, detail="Word of the day not found")
        word_id = word_of_day.word.id
        
        audio_bytes = await audio_file.read()

        # 1. Send .wav file to blob store
        wav_file = self.create_wav_file(audio_bytes)
        s3_key = upload_wav_to_s3(wav_file)
        
        # 2. Create word of day attempt entries and recording entries
        attempt = uow.attempts.upsert(Attempt(user_id=user.id))
        uow.word_of_day_attempts.upsert(WordOfDayAttempt(id=attempt.id, user_id=user.id, word_of_day_id=word_of_day_id))
        recording = uow.recordings.upsert(Recording(attempt_id=attempt.id, s3_key=s3_key))
        uow.commit()
        
        return self.get_attempt_feedback(wav_file, uow, user, word_id, recording.id)

