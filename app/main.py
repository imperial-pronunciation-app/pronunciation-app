from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_home():
    return {"Hello": "James"}


if __name__ == "__main__":
    pass
