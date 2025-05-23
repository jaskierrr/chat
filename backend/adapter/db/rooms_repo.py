from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.adapter.db.postgres import Message, Room, user_room
from backend.const import POSTGRES_CONN
from backend.container import main_container
from backend.entrypoints.schemas.request_schemas import SendMessage


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

    async def get_rooms_list(self, target_user_id) -> list[Room] | None:
        async with self.session() as session:
            sql = select(Room).join(user_room).where(user_room.c.user_id == target_user_id)
            result = (await session.execute(sql)).scalars().all()
            await session.commit()

        return result

    async def get_messages_by_room_id(self, room_id) -> Room | None:
        async with self.session() as session:
            # sql = select(Room).join(Message).where(Room.id == room_id).join(user_room).where()
            sql = select(Message).where(Message.room_id == room_id).options(joinedload(Message.user), joinedload(Message.room))
            print('SQL')
            print(sql)
            result = (await session.execute(sql)).scalars().all()
            print(result)
            await session.commit()

        return result

    # async def send_message(self, user_id, room_id, body):
    async def send_message(self, message: SendMessage):
        async with self.session() as session:
            # sql = insert(Message).values(user_id=user_id, room_id=room_id, body=body)
            # result = (await session.execute(sql)).scalars().all()
            new_message = Message(**message.model_dump())
            session.add(new_message)
            await session.commit()

        return new_message


    def _get_session(self):
        if session := main_container.get(POSTGRES_CONN):
            return session
        raise RuntimeError("Session not found")
