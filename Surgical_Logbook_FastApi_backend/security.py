from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from database import get_session
from typing import Annotated
from sqlmodel import Session
from models import User
from config import settings

SessionDep = Annotated[Session, Depends(get_session)]

# hashing and verifying passwords
pwd_context = CryptContext(schemes=["bcrypt"],bcrypt__default_rounds=12,deprecated="auto",bcrypt__ident="2b")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# oauth2


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authentication/login")

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")

        if sub is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return sub

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(session:SessionDep,token:str = Depends(oauth2_scheme)):
    
    user_id = verify_access_token(token)
    user = session.get(User,int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

def get_current_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user