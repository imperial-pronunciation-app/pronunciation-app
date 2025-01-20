from dotenv import load_dotenv
from fastapi import FastAPI

from app.models import (  # noqa F401
    ModelFeedback,
    Phoneme,
    Recording,
    RecordingFeedback,
    RecordingPhonemes,
    User,
    Word,
    WordPhonemes,
)
from app.routers import random_word_router, recording_router, satisfaction_router

load_dotenv()

app = FastAPI()

# Set up routers
app.include_router(random_word_router)
app.include_router(recording_router)
app.include_router(satisfaction_router)


@app.get("/")
def read_home():
    return {"Hello": "World"}


if __name__ == "__main__":
    pass
