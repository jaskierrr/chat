from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status
import jwt
from jwt.exceptions import InvalidTokenError
from chat.adapter.db.user_repo import UserRepo
from config import config

from chat.entrypoint.shemas.request_shemas import UserLogin


async def authenticate_user(db: UserRepo, user: UserLogin):
    # запрос в базу с проверкой пароля

    user = await db.get(user.login)
    print(user)

    return True


def encodeJWT(user: UserLogin):
    if config.auth.ttl:
        exp = datetime.now(tz=timezone.utc) + timedelta(seconds=config.auth.ttl)
    else:
        exp = datetime.now(tz=timezone.utc) + timedelta(minutes=30)

    payload = {"sub": user.login, "exp": exp}

    return jwt.encode(payload, config.auth.secret, "HS512")


def decodeJWT(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.auth.secret, "HS512")
        if payload.get("sub") is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    # user = get_user(payload.username)
    #     # сходить в базу и вернуть юзера
    # if user is None:
    #     raise credentials_exception
    #
    # return user

    print('Token correct')
    return True
