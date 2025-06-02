from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.adapter.db.postgres import Message, Room, user_room
from backend.const import POSTGRES_CONN
from backend.container import main_container
from backend.entrypoints.schemas.request_schemas import SendMessage
from backend.entrypoints.schemas.ws_schemas import WSMessage, WSMessageBodyCreateRoom


class RoomsRepo:
    def __init__(self) -> None:
        self.session: AsyncSession = self._get_session()

    async def create_room(self, create_room_data: WSMessageBodyCreateRoom):
        async with self.session() as session:
            room = Room(name=f"Room from: {create_room_data.src_user_id}")
            session.add(room)
            print(room)

            await session.commit()

            create_room_data.other_users_ids.append(create_room_data.src_user_id)

            user_room_data = [
                {"room_id": room.id, "user_id": user_id}
                for user_id in create_room_data.other_users_ids
            ]

            result = await session.execute(
                insert(user_room).returning(user_room), user_room_data
            )
            print(result)

            await session.commit()
        return room

    async def get_rooms_list(self, target_user_id) -> list[Room] | None:
        async with self.session() as session:
            sql = (
                select(Room).join(user_room).where(user_room.c.user_id == target_user_id)
            )
            result = (await session.execute(sql)).scalars().all()
            await session.commit()

        return result

    async def get_room(self, room_id) -> Room | None:
        async with self.session() as session:
            sql = select(Room).where(Room.id == room_id)
            result = (await session.execute(sql)).scalar_one_or_none()
            await session.commit()

        return result

    async def get_messages_by_room_id(self, room_id) -> Message | None:
        async with self.session() as session:
            sql = (
                select(Message)
                .where(Message.room_id == room_id)
                .options(joinedload(Message.user), joinedload(Message.room))
            )
            print("SQL")
            print(sql)
            result = (await session.execute(sql)).scalars().all()
            print(result[0].user.id, result[0].room.id)
            await session.commit()

        return result

    # async def send_message(self, user_id, room_id, body):
    async def send_message(self, message: WSMessage):
        async with self.session() as session:
            # sql = insert(Message).values(user_id=user_id, room_id=room_id, body=body)
            # result = (await session.execute(sql)).scalars().all()
            new_message = Message(
                text=message.body.text,
                user_id=message.body.user.id,
                room_id=message.body.room.id,
                created_at=message.head.timestamp,
            )
            print(new_message.__dict__)
            # session.add(new_message)
            # await session.commit()

        # return new_message

    def _get_session(self):
        if session := main_container.get(POSTGRES_CONN):
            return session
        raise RuntimeError("Session not found")
