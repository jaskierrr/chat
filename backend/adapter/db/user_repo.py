from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.adapter.db.postgres import User
from backend.const import POSTGRES_CONN
from backend.container import main_container
from backend.entrypoints.schemas.request_schemas import UserLogin


class UserRepo:
    def __init__(self) -> None:
        self.session: AsyncSession = self._get_session()

    async def create(self, user_data: UserLogin):
        async with self.session() as session:
            new_user = User(**user_data.model_dump())
            user = session.add(new_user)
            await session.commit()

        return user

    async def get(self, login) -> User:
        async with self.session() as session:
            sql = select(User).where(User.login == login)
            result = await session.execute(sql)
            # await session.commit()

        return result.scalar_one()

    def _get_session(self):
        if session := main_container.get(POSTGRES_CONN):
            return session
        raise RuntimeError("Session not found")
