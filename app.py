from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Field, SQLModel, create_engine, Session, select
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

app = FastAPI()

def get_session():
    with Session(engine) as session:
        yield session

SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    if not session.exec(select(User)).first():
        user = User(name="James")
        session.add(user)
        session.commit()

@app.get("/")
def read_home(session: Session = Depends(get_session)):
    users = session.exec(select(User)).first()
    if not user:
        raise HTTPException(status_code=404, detail="No users found")
    return {"name": user.name}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)