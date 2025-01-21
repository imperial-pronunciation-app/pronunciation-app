from typing import Dict

from fastapi import FastAPI




app = FastAPI()


@app.get("/")
def read_home():  # would be a Pydantic return type normally
    return {"Hello": "James"}


if __name__ == "__main__":
    pass
