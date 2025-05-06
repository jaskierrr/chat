from fastapi import Response
from fastapi.responses import JSONResponse

from backend.auth.auth import decodeJWT


class AuthService:
    def validate_token(self, request):
        cookies = request.headers.get("cookie")
        if cookies:
            for cookie in cookies:
                if "token=" in cookie:
                    token = cookie.split("=")[1]
                else:
                    return Response(status_code=404)

        # TODO: переделать, писать такой try/except неправильно
        try:
            user_id = {"id": decodeJWT(token)['user_id']}
            print("token", user_id)
            return JSONResponse(content=user_id, status_code=200)
        except Exception:
            return Response(status_code=404)
