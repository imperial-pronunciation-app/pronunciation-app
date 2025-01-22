from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict

from fastapi import FastAPI
from transformers import pipeline
from transformers.pipelines import Pipeline

from app.routers.random_word import router


ml_models: Dict[str, Pipeline] = {}

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


app.include_router(router)

if __name__ == "__main__":
    pass
