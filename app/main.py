from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict

from fastapi import FastAPI
from transformers import pipeline

from app.routers.random_word import router as random_word_router
from app.routers.recording import ml_models
from app.routers.recording import router as recording_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Before app startup
    ml_models["whisper"] = pipeline(task="automatic-speech-recognition", model="openai/whisper-tiny.en")
    yield
    # After app shutdown
    ml_models.clear()

app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_home() -> Dict[str, str]:  # would be a Pydantic return type normally
    return {"Hello": "James"}


app.include_router(random_word_router)
app.include_router(recording_router)

if __name__ == "__main__":
    pass
