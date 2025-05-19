from datetime import datetime, timezone
from backend.adapter.db.rooms_repo import RoomsRepo
from backend.entrypoints.schemas.ws_response import WSMessageBodyGetRoomsList
from backend.entrypoints.schemas.ws_schemas import (
    WSMessage,
    WSMessageBodyRoomId,
    WSMessageBodyRoomIdText,
    WSMessageBodyUserId,
    WSMessageHead,
    WSMessageType,
)


class CantGetRooms(Exception):
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
                    type=WSMessageType.response,
                    command=message.head.command,
                    timestamp=datetime.now(tz=timezone.utc),
                )
                response_msg = WSMessage(head=head, body=body)
                print(response_msg)
        except Exception as err:
            raise CantGetRooms("\n\nCant get rooms for user", err)

        # ЭТО ОТВЕТ ДЛЯ FASTAPI, ПЕРЕДЕЛАТЬ НА JSON ДЛЯ WS (ТИПА head, body)
        return response_msg

    async def get_room(self, message_data: WSMessage) -> WSMessage:
        message = WSMessage[WSMessageBodyRoomId].model_validate(message_data)
        room_repo: RoomsRepo = RoomsRepo()
        print(f"{message=}")
        try:
            if room := await room_repo.get_messages_by_room_id(message.body.id):
                print("in service", room)
            else:
                raise CantGetRooms("\n\nCant get messages by room id")
        except Exception as err:
            raise CantGetRooms("\n\nCant get messages by room id", err)

    async def send_message(self, user_id, message_data: WSMessage) -> WSMessage:
        print(message_data)
        message = WSMessage[WSMessageBodyRoomIdText].model_validate(message_data)
        room_repo: RoomsRepo = RoomsRepo()
        print(f"{message=}")
        try:
            if room := await room_repo.send_message(
                user_id, message.body.room_id, message.body.text
            ):
                print("in service", room)
            else:
                raise CantGetRooms("\n\nCant write message in DB")
        except Exception as err:
            raise CantGetRooms("\n\nCant write message in DB", err)
