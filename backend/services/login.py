from sqlalchemy.exc import NoResultFound

from backend.adapter.db.user_repo import UserRepo
from backend.auth.auth import authenticate_user
from backend.entrypoints.schemas.request_schemas import UserLogin

# user_repo = UserRepo()


class LoginService:
    async def login_user(self, user_data: UserLogin, user_repo: UserRepo):
        try:
            user = await authenticate_user(user_repo, user_data)
        except NoResultFound:
            raise NoResultFound

        return user
