import os
import uuid
from typing import List, Tuple

import requests
from fastapi import Depends, HTTPException, UploadFile

from app.config import get_settings
from app.crud.unit_of_work import UnitOfWork, get_unit_of_work
from app.models.attempt import Attempt
from app.models.exercise_attempt import ExerciseAttempt
from app.models.recording import Recording
from app.models.user import User
from app.models.word import Word
from app.models.word_of_day_attempt import WordOfDayAttempt
from app.schemas.attempt import AttemptResponse
from app.schemas.model_api import InferPhonemesResponse
from app.schemas.phoneme import PhonemePublic
from app.services.pronunciation import PronunciationService
from app.services.unit import UnitService
from app.services.user import UserService
from app.users import current_active_user
from app.utils.s3 import upload_wav_to_s3


class AttemptService:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def create_wav_file(self, audio_bytes: bytes) -> str:
        temp_file = uuid.uuid4()
        filename = f"{temp_file}.wav"
        with open(filename, "bx") as f:
            f.write(audio_bytes)
        return filename

    async def dispatch_to_model(self, audio_file: UploadFile) -> Tuple[List[str], str]:
        audio_bytes = await audio_file.read() # TODO: Check if await is needed
        wav_file = self.create_wav_file(audio_bytes)
        with open(wav_file, "rb") as f:
            files = {"audio_file": f}

            print(get_settings().MODEL_API_URL)
            model_response = requests.post(f"{get_settings().MODEL_API_URL}/api/v1/eng/infer_phonemes", files=files)

        model_response.raise_for_status()

        model_data = InferPhonemesResponse.model_validate(model_response.json())

        return model_data.phonemes, wav_file

    # def get_attempt_feedback(
    #     self, wav_file: str, uow: UnitOfWork, user: User, word: Word, recording_id: int
    # ) -> AttemptResponse:
    #     # 3. Dispatch recording to ML backend
    #     # inferred_phoneme_strings = self.dispatch_to_model(wav_file)

    #     # 4. Form feedback based on model response
    #     # aligned_phonemes, score = PronunciationService(uow).evaluate_pronunciation(word, inferred_phoneme_strings)

    #     # # 5. Update user xp based on feedback
    #     # user_service = UserService(uow)
    #     # xp_gain = user_service.update_xp_with_boost(user, score)

    #     # 6. Delete temporary file
    #     # os.remove(wav_file)

    #     # 7. Serve response to user
    #     return AttemptResponse(recording_id=recording_id, score=score, phonemes=aligned_phonemes, xp_gain=xp_gain)

    # async def post_helper(self, score: int, audio_file: UploadFile, user: User, uow: UnitOfWork) -> tuple[str, int, int]:
    #     # audio_bytes = await audio_file.read()
    #     # wav_file = self.create_wav_file(audio_bytes)
    #     # s3_key = upload_wav_to_s3(wav_file)
    #     # attempt = self._uow.attempts.upsert(Attempt(user_id=user.id, score=score))

    #     # recording = uow.recordings.upsert(Recording(attempt_id=attempt.id, s3_key=s3_key))

    #     return (wav_file, recording.id, attempt.id)

    # async def post_exercise_attempt(
    #     self,
    #     audio_file: UploadFile,
    #     exercise_id: int,
    #     uow: UnitOfWork = Depends(get_unit_of_work),
    #     user: User = Depends(current_active_user),
    # ) -> AttemptResponse:
    #     exercise = uow.exercises.find_by_id(id=exercise_id)
    #     if not exercise:
    #         raise HTTPException(status_code=404, detail="Exercise not found")

    #     # 1. Send .wav file to blob store and create recording entry
    #     (wav_file, recording_id, attempt_id) = await self.post_helper(audio_file, user, uow)

    #     # 2. Create exercise attempt entries
    #     # uow.exercise_attempts.upsert(ExerciseAttempt(id=attempt_id, user_id=user.id, exercise_id=exercise_id))
    #     # uow.commit()

    #     # feedback = self.get_attempt_feedback(wav_file, uow, user, exercise.word, recording_id)
    
    #     # 3. Generate recap lesson if this is the last exercise of the last lesson
    #     # unit_service = UnitService(uow)
    #     # if unit_service._is_completed_by(exercise.lesson.unit, user) and uow.lessons.find_recap_by_user_id_and_unit_id(user.id, exercise.lesson.unit_id) is None:
    #     #     print("Generating recap lesson")
    #     #     unit_service.generate_recap_lesson(exercise.lesson.unit, user)
        
    #     return feedback

    # async def post_word_of_day_attempt(
    #     self,
    #     audio_file: UploadFile,
    #     word_of_day_id: int,
    #     uow: UnitOfWork = Depends(get_unit_of_work),
    #     user: User = Depends(current_active_user),
    # ) -> AttemptResponse:
    #     word_of_day = uow.word_of_day.find_by_id(id=word_of_day_id)
    #     if not word_of_day:
    #         raise HTTPException(status_code=404, detail="Word of the day not found")
        
        

    #     # 1. Send .wav file to blob store and create recording entry
    #     (wav_file, recording_id, attempt_id) = await self.post_helper(audio_file, user, uow)

    #     # 2. Create word of day attempt entries and recording entries
    #     uow.word_of_day_attempts.upsert(WordOfDayAttempt(id=attempt_id, user_id=user.id, word_of_day_id=word_of_day_id))
    #     uow.commit()

    #     return self.get_attempt_feedback(wav_file, uow, user, word_of_day.word, recording_id)
    
    async def get_attempt_feedback(
            self,
            audio_file: UploadFile,
            word: Word
    ) -> Tuple[List[Tuple[PhonemePublic | None, PhonemePublic | None]], int, str]:
        inferred_phoneme_strings, wav_file = await self.dispatch_to_model(audio_file)
        aligned_phonemes, score = PronunciationService(self._uow).evaluate_pronunciation(word, inferred_phoneme_strings)
        return aligned_phonemes, score, wav_file
    
    def save_to_s3(self, wav_file: str) -> str:
        s3_key = upload_wav_to_s3(wav_file)
        os.remove(wav_file)
        return s3_key
    
    def create_attempt_and_recording(self, user: User, score: int, s3_key: str) -> Tuple[int, int]:
        attempt = self._uow.attempts.upsert(Attempt(user_id=user.id, score=score))
        recording = self._uow.recordings.upsert(Recording(attempt_id=attempt.id, s3_key=s3_key))
        return attempt.id, recording.id
    
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
        
        # 1. Send .wav file to model for response
        aligned_phonemes, score, wav_file = await self.get_attempt_feedback(audio_file, exercise.word)
        user_service = UserService(uow)
        xp_gain = user_service.update_xp_with_boost(user, score)

        # 2. Save .wav file to s3
        s3_key = self.save_to_s3(wav_file)

        # 3. Create attempt and recording entries
        attempt_id, recording_id = self.create_attempt_and_recording(user, score, s3_key)
        uow.exercise_attempts.upsert(ExerciseAttempt(id=attempt_id, user_id=user.id, exercise_id=exercise_id))
        uow.commit()

        # 4. Generate recap lesson if this is the last exercise of the last lesson
        unit_service = UnitService(uow)
        if unit_service._is_completed_by(exercise.lesson.unit, user) and uow.lessons.find_recap_by_user_id_and_unit_id(user.id, exercise.lesson.unit_id) is None:
            unit_service.generate_recap_lesson(exercise.lesson.unit, user)

        return AttemptResponse(recording_id=recording_id, score=score, phonemes=aligned_phonemes, xp_gain=xp_gain)
    
    async def post_word_of_day_attempt(
        self,
        audio_file: UploadFile,
        word_of_day_id: int,
        uow: UnitOfWork = Depends(get_unit_of_work),
        user: User = Depends(current_active_user),
    ) -> AttemptResponse:
        word_of_day = uow.word_of_day.find_by_id(id=word_of_day_id)
        if not word_of_day:
            raise HTTPException(status_code=404, detail="Word of the day not found")
        
        aligned_phonemes, score, wav_file = await self.get_attempt_feedback(audio_file, word_of_day.word)
        user_service = UserService(uow)
        xp_gain = user_service.update_xp_with_boost(user, score)

        s3_key = self.save_to_s3(wav_file)

        attempt_id, recording_id = self.create_attempt_and_recording(user, score, s3_key)
        uow.word_of_day_attempts.upsert(WordOfDayAttempt(id=attempt_id, user_id=user.id, word_of_day_id=word_of_day_id))
        uow.commit()

        return AttemptResponse(recording_id=recording_id, score=score, phonemes=aligned_phonemes, xp_gain=xp_gain)
