from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import hashlib

from config.database import SessionLocal
from models.user import User

router = APIRouter()

import os

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

security = HTTPBearer()


class UserRegister(BaseModel):
    name: str
    email: str
    password: str
    age: int
    gender: str


class UserLogin(BaseModel):
    email: str
    password: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Password hashing
def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain, hashed):
    return hashlib.sha256(plain.encode()).hexdigest() == hashed


# Create JWT
def create_token(data: dict):
    expire = datetime.utcnow() + timedelta(hours=2)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


# Get current user
def get_current_user(token=Depends(security), db: Session = Depends(get_db)):

    credentials_exception = HTTPException(
        status_code=401, detail="Invalid authentication credentials"
    )

    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception

        user = db.query(User).filter(User.email == email).first()

        if user is None:
            raise credentials_exception

        return {"id": user.id, "name": user.name, "email": user.email}

    except JWTError:
        raise credentials_exception


# Register
@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.email == user.email).first()

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = hash_password(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed,
        age=user.age,
        gender=user.gender,
    )

    db.add(new_user)
    db.commit()

    return {"message": "User registered successfully"}


# Login
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # CREATE TOKEN HERE
    token = create_token({"sub": db_user.email})

    return {"access_token": token, "token_type": "bearer"}
