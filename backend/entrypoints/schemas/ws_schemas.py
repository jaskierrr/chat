from datetime import datetime
from typing import Generic, TypeVar
from pydantic import BaseModel
from enum import StrEnum

class WSEventType(StrEnum):
    get_rooms_list = "/get_rooms_list"
    get_room = "/get_room"
    send_message = "/send_message"
    get_users_list = "/get_users_list"


class WSMessageBodyUserId(BaseModel):
    id: str


class WSMessageBodyRoomId(BaseModel):
    id: str


class WSMessageBodyRoomIdText(BaseModel):
    room_id: str
    text: str


class WSMessageHead(BaseModel):
    event: WSEventType | None = None
    timestamp: datetime
    token: str | None = None


WSMessageBodyType = TypeVar("WSMessageBodyType")


class WSMessage(BaseModel, Generic[WSMessageBodyType]):
    head: WSMessageHead | None = None
    body: WSMessageBodyType | None = None
