from datetime import datetime, timezone
import uuid
from backend.adapter.db import rooms_repo
from backend.adapter.db.rooms_repo import RoomsRepo
from backend.adapter.db.user_repo import UserRepo
from backend.entrypoints.schemas.ws_response import (
    RoomSchema,
    WSMessageBodyGetRoom,
    WSMessageBodyGetRoomsList,
    WSMessageBodyGetUsersList,
)
from backend.entrypoints.schemas.ws_schemas import (
    WSMessage,
    WSMessageBodyCreateRoom,
    WSMessageBodyMessage,
    WSMessageBodyRoomId,
    WSMessageBodyUserId,
    WSMessageHead,
)


class CantGetSomething(Exception):
    pass


class CantWriteMsg(Exception):
    pass


class WSService:
    def __init__(self) -> None:
        self.user_repo = UserRepo()
        self.room_repo = RoomsRepo()

    async def get_rooms_list(self, user_id, message_data: WSMessage) -> WSMessage:
        message = WSMessage[WSMessageBodyUserId].model_validate(message_data)
        print(f"{message=}")
        try:
            if rooms := await self.room_repo.get_rooms_list(message.body.id):
                body = WSMessageBodyGetRoomsList.unpack_rooms(rooms)
                head = WSMessageHead(
                    event=message.head.event,
                    timestamp=datetime.now(tz=timezone.utc),
                )
                response_msg = WSMessage(head=head, body=body)
                print(response_msg)
        except Exception as err:
            raise CantGetSomething("\n\nCant get rooms for user", err)

        return response_msg

    async def get_users_list(self, message_data: WSMessage) -> WSMessage:
        message = WSMessage[WSMessageBodyUserId].model_validate(message_data)
        print(f"{message=}")
        try:
            if users := await self.user_repo.get_users_list(message.body.id):
                body = WSMessageBodyGetUsersList.unpack_users(users)
                head = WSMessageHead(
                    event=message.head.event,
                    timestamp=datetime.now(tz=timezone.utc),
                )
                response_msg = WSMessage(head=head, body=body)
                print(response_msg)
        except Exception as err:
            raise CantGetSomething("\n\nCant get users for user", err)

        return response_msg

    async def get_room(self, message_data: WSMessage) -> WSMessage:
        message = WSMessage[WSMessageBodyRoomId].model_validate(message_data)
        print(f"{message=}")
        try:
            messages = await self.room_repo.get_messages_by_room_id(message.body.id)
            print("in service", messages)

            room = await self.room_repo.get_room(message.body.id)

            body = WSMessageBodyGetRoom.unpack_messages(messages, room)

            head = WSMessageHead(
                event=message.head.event,
                timestamp=datetime.now(tz=timezone.utc),
            )
            response_msg = WSMessage(head=head, body=body)
            print(response_msg)
        except Exception as err:
            raise CantGetSomething("\n\nCant get messages by room id", err)

        return response_msg

    async def create_room(self, message_data: WSMessage) -> WSMessage:
        message = WSMessage[WSMessageBodyCreateRoom].model_validate(message_data)
        print(f"{message=}")
        try:
            if room := await self.room_repo.create_room(message.body):

                body = RoomSchema(id=room.id, name=room.name)
                head = WSMessageHead(
                    event=message.head.event,
                    timestamp=datetime.now(tz=timezone.utc),
                )
                response_msg = WSMessage(head=head, body=body)
                print(response_msg)

                return response_msg
            else:
                raise CantGetSomething("\n\nCant create room")
        except Exception as err:
            raise CantGetSomething("\n\nCant create room", err)

    async def send_message(
        self, message_data: WSMessage
    ) -> tuple[WSMessage, list[uuid.UUID]]:
        print(message_data)
        message = WSMessage[WSMessageBodyMessage].model_validate(message_data)
        print(f"{message=}")
        try:
            if msg := await self.room_repo.send_message(message):
                print("in service", msg)

                messages = await self.room_repo.get_messages_by_room_id(
                    message.body.message.room_id
                )

                room = await self.room_repo.get_room(message.body.message.room_id)
                body = WSMessageBodyGetRoom.unpack_messages(messages, room)
                head = WSMessageHead(
                    event=message.head.event,
                    timestamp=datetime.now(tz=timezone.utc),
                )

                res = WSMessage(head=head, body=body)

                users_ids = await self.room_repo.get_users_ids_by_room_id(
                    message.body.message.room_id, message.body.message.user_id
                )

            else:
                raise CantWriteMsg("\n\nCant write message in DB", msg)
        except Exception as err:
            raise CantWriteMsg("\n\nCant write message in DB", err)

        return res, users_ids
