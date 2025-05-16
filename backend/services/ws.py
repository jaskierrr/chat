from datetime import datetime, timezone
from backend.adapter.db.rooms_repo import RoomsRepo
from backend.entrypoints.schemas.ws_response import WSMessageBodyGetRooms
from backend.entrypoints.schemas.ws_schemas import WSMessage, WSMessageBodyUserId, WSMessageHead, WSMessageType


class CantGetRooms(Exception):
    pass

class WSService:

    async def get_rooms_list(self, user_id, message_data: WSMessage) -> WSMessage:
                message = WSMessage[WSMessageBodyUserId].model_validate(message_data)
                room_repo: RoomsRepo = RoomsRepo()
                print(f"{message.body.id=}")
                try:
                    rooms = await room_repo.get(message.body.id)
                    body = WSMessageBodyGetRooms.unpack_rooms(rooms)
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

