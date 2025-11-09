from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from fastapi.security import HTTPBasic

from passlib.context import CryptContext
from src.db.session import redis
from src.db.models import UserRegister
import uuid
import time
import json


router = APIRouter()
security = HTTPBasic()


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

MAX_BCRYPT_LENGTH = 72


@router.post("/register")
async def register(
    user: UserRegister
):
    if await redis.exists(f"user:{user.username}"):
        raise HTTPException(
            status_code=400,
            detail="Username already exist"
        )
    password = user.password
    hashed_pw = pwd_context.hash(password)
    await redis.set(f"user:{user.username}", hashed_pw)
    return{"message": "registered successfully"}


@router.post("/login")
async def login(
    response: Response, 
    user: UserRegister,
    ):
    hashed_pw = await redis.get(f"user:{user.username}")
    if not hashed_pw or not pwd_context.verify(user.password, hashed_pw):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    
    session_id = uuid.uuid4().hex

    session_data = {"username": user.username, "login_at": time.time()}

    await redis.set(f"session:{session_id}", json.dumps(session_data), ex=10)
    response.set_cookie("session_id", session_id, httponly=True)
    return {"message": "Login successful"}


async def get_current_user(session_id: str = Cookie(None)):
    if not session_id:
        raise HTTPException(
            status_code=401,
            detail="Not Authorized"
        )
    session_data = await redis.get(f"session:{session_id}")
    if not session_data:
        raise HTTPException(
            status_code=401, 
            detail="Session expired",
            )
    data = json.loads(session_data)
    return data["username"]


@router.get("/profile")
def profile(username: str = Depends(get_current_user)):
    return {"message": f"Hi {username}"}


@router.post("/logout")
async def logout(response: Response, session_id: str = Cookie(None)):
    if session_id:
        await redis.delete(f"session:{session_id}")
        response.delete_cookie("session_id")
    return {"message": "Successfuly logged out"}