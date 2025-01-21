from typing import Dict

from fastapi import FastAPI

from app.routers.random_word import router


app = FastAPI()


@app.get("/")
def read_home() -> Dict[str, str]:  # would be a Pydantic return type normally
    return {"Hello": "James"}


app.include_router(router)

if __name__ == "__main__":
    pass
