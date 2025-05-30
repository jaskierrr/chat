from datetime import datetime, timezone
from backend.adapter.db.rooms_repo import RoomsRepo
from backend.adapter.db.user_repo import UserRepo
from backend.entrypoints.schemas.request_schemas import SendMessage
from backend.entrypoints.schemas.ws_response import RoomSchema, WSMessageBodyGetRoomsList, WSMessageBodyGetUsersList
from backend.entrypoints.schemas.ws_schemas import (
    WSMessage,
    WSMessageBodyCreateRoom,
    WSMessageBodyRoomId,
    WSMessageBodyRoomIdText,
    WSMessageBodyUserId,
    WSMessageHead,
)


class CantGetSomething(Exception):
    pass

class CantWriteMsg(Exception):
    pass


class WSService:
    async def get_rooms_list(self, user_id, message_data: WSMessage) -> WSMessage:
        message = WSMessage[WSMessageBodyUserId].model_validate(message_data)
        room_repo: RoomsRepo = RoomsRepo()
        print(f"{message=}")
        try:
            if rooms := await room_repo.get_rooms_list(message.body.id):
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
        user_repo: UserRepo = UserRepo()
        print(f"{message=}")
        try:
            if users := await user_repo.get_users_list(message.body.id):
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
        room_repo: RoomsRepo = RoomsRepo()
        print(f"{message=}")
        try:
            if room := await room_repo.get_messages_by_room_id(message.body.id):
                print("in service", room)
                return room
            else:
                raise CantGetSomething("\n\nCant get messages by room id")
        except Exception as err:
            raise CantGetSomething("\n\nCant get messages by room id", err)

    async def create_room(self, message_data: WSMessage) -> WSMessage:
        message = WSMessage[WSMessageBodyCreateRoom].model_validate(message_data)
        room_repo: RoomsRepo = RoomsRepo()
        print(f"{message=}")
        print('\n\n\n')
        try:
            if room := await room_repo.create_room(message.body):
                print("in service", room)

                body = RoomSchema(id=room.id, name= room.name)
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

    async def send_message(self, user_id, message_data: WSMessage) -> WSMessage:
        print(message_data)
        message = WSMessage[WSMessageBodyRoomIdText].model_validate(message_data)
        room_repo: RoomsRepo = RoomsRepo()
        print(f"{message=}")
        message_data = SendMessage(user_id=user_id, room_id=message.body.room_id, created_at=datetime.now(), body=message.body.text)
        try:
            if msg := await room_repo.send_message(
                # user_id, message.body.room_id, message.body.text
                message_data
            ):
                print("in service", msg)

                head = WSMessageHead(
                    event=message.head.event,
                    timestamp=datetime.now(tz=timezone.utc),
                )

                res = WSMessage(head=head, body=None)
            else:
                raise CantWriteMsg("\n\nCant write message in DB", msg)
        except Exception as err:
            raise CantWriteMsg("\n\nCant write message in DB", err)
        return res
