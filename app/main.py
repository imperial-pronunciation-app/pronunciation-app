from typing import Dict

from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.random_word import router as random_word_router
from app.routers.recording import router as recording_router
from app.routers.users import router as users_router


app = FastAPI()


@app.get("/")
def read_home() -> Dict[str, str]:  # would be a Pydantic return type normally
    return {"Hello": "James"}


app.include_router(random_word_router)
app.include_router(recording_router)
app.include_router(auth_router)
app.include_router(users_router)

if __name__ == "__main__":
    pass
