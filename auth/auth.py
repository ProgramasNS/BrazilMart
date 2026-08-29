#That's the middleware functions file, where authentications are made.
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import encode
from dotenv import load_dotenv
from os import getenv

import jwt
from pydantic import BaseModel
from sqlalchemy import UUID

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_token(data: dict):
    encoded = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=180)
    encoded.update({"exp": expire})
    return encode(encoded, getenv("JWT_SECRET"), "HS256")

def verify_token(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, getenv("JWT_SECRET"), algorithms=["HS256"])
        nickname = payload.get("sub")

        if nickname is None:
            raise credentials_exception

        return nickname 
    except jwt.PyJWTError:
        raise credentials_exception

class TokenPayload(BaseModel):
    id: Optional[UUID] = None
    sub: Optional[str] = None    
    nickname: Optional[str] = None
    role: Optional[str] = None  