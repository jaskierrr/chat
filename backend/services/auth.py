from typing import Dict
from backend.adapter.db.user_repo import UserRepo
from backend.auth.auth import decodeJWT


class JWTNotFound(Exception):
    pass


class AuthService:
    def __init__(self) -> None:
        self.user_repo = UserRepo()

    def validate_token(self, request) -> Dict[str, str]:
        cookies = request.headers.get("cookie")
        token = ''
        if cookies:
            cookie_list = cookies.split(';')
            for cookie in cookie_list:
                if "token=" in cookie:
                    token = cookie.split("=")[1]

            if not token:
                raise JWTNotFound("JWT not found in cookies from request")

        return decodeJWT(self.user_repo, token)

    def validate_token_from_ws(self, token) -> Dict[str, str]:
        if not token:
                raise JWTNotFound("JWT not found in cookies from request")

        return decodeJWT(self.user_repo, token)       
