from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.adapter.db.postgres import Room, user_room
from backend.const import POSTGRES_CONN
from backend.container import main_container


class RoomsRepo:
    def __init__(self) -> None:
        self.session: AsyncSession = self._get_session()

    # async def create(self, user_data: UserLogin):
    #     async with self.session() as session:
    #         new_user = User(**user_data.model_dump())
    #         user = session.add(new_user)
    #         await session.commit()
    #
    #     return user

    async def get(self, target_user_id) -> list[Room]:
        async with self.session() as session:
            sql = select(Room).join(user_room).where(user_room.c.user_id == target_user_id)
            result = (await session.execute(sql)).scalars().all()
            await session.commit()

        return result

    def _get_session(self):
        if session := main_container.get(POSTGRES_CONN):
            return session
        raise RuntimeError("Session not found")
