from typing import Dict
from backend.auth.auth import decodeJWT


class JWTNotFound(Exception):
    pass


class AuthService:
    def validate_token(self, request) -> Dict[str, str]:
        cookies = request.headers.get("cookie")
        print(f'{cookies=}')
        token = ''
        if cookies:
            cookie_list = cookies.split(';')
            for cookie in cookie_list:
                if "token=" in cookie:
                    token = cookie.split("=")[1]

            if not token:
                raise JWTNotFound("JWT not found in cookies from request")

        return decodeJWT(token)
