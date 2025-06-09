from sqlalchemy.exc import NoResultFound

from backend.adapter.db.user_repo import UserRepo
from backend.auth.auth import authenticate_user
from backend.entrypoints.schemas.request_schemas import UserLogin


class LoginService:
    def __init__(self) -> None:
        self.user_repo = UserRepo()

    async def login_user(self, user_data: UserLogin):
        try:
            user = await authenticate_user(self.user_repo, user_data)
        except NoResultFound:
            raise NoResultFound

        return user
