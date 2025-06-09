from typing import Dict
import jwt
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status
from jwt.exceptions import InvalidTokenError
from backend.adapter.db.postgres import User
from backend.adapter.db.user_repo import UserRepo
from backend.config import config



async def authenticate_user(db: UserRepo, user: User):
    user = await db.get(user.username)

    return user


def encodeJWT(user: User):
    if config.auth.ttl:
        exp = datetime.now(tz=timezone.utc) + timedelta(seconds=config.auth.ttl)
        pass
    else:
        exp = datetime.now(tz=timezone.utc) + timedelta(minutes=30)

    payload = {"username": user.username, "user_id": str(user.id), "exp": exp}

    return jwt.encode(payload, config.auth.secret, "HS512")


def decodeJWT(user_repo: UserRepo, token: str) -> Dict[str, str]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    credentials_exception_for_sub = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="sub field in token is None",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.auth.secret, "HS512")
        if payload.get("username") is None or payload.get("user_id") is None:
            raise credentials_exception_for_sub
    except InvalidTokenError:
        raise credentials_exception

    try:
        user = user_repo.get(payload.get('username'))
        if user is None:
            raise credentials_exception
    except Exception:
        raise

    print("Token correct", token)
    return payload
