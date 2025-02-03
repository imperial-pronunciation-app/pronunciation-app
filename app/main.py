from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict

from fastapi import FastAPI
from transformers import pipeline

from app.routers import routers
from app.routers.recording import ml_models


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """This function and ml_models global variable should be removed when ml models are deployed in a separate microservice."""
    
    # Before app startup
    ml_models["whisper"] = pipeline(task="automatic-speech-recognition", model="openai/whisper-tiny.en")
    yield
    # After app shutdown
    ml_models.clear()

app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_home() -> Dict[str, str]:  # would be a Pydantic return type normally
    return {"Hello": "James"}


for router in routers:
    app.include_router(router)


if __name__ == "__main__":
    pass
