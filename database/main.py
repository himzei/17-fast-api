from fastapi import FastAPI, Depends
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session
from pydantic import BaseModel

app = FastAPI()

Base = declarative_base()
DATABASE_URL = "postgresql://postgres.apbehdgajtfwomvfommg:3izbkEmGzfEC78c0@aws-1-ap-northeast-2.pooler.supabase.com:6543/postgres"
engine = create_engine(DATABASE_URL)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String)

class UserCreate(BaseModel):
    username: str
    email: str

def get_db(): 
    db = Session(engine)
    try: 
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {
        "message": "hi fastapi"
    }


@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(username=user.username, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "id": new_user.id, 
        "username": new_user.username, 
        "email": new_user.email
    }