from datetime import datetime
from typing import Generic, TypeVar
from pydantic import BaseModel
from enum import StrEnum


class WSMessageType(StrEnum):
    command = "command"
    message = "message"
    response = "response"


class WSCommandType(StrEnum):
    get_rooms_list = "/get_rooms_list"
    get_room = "/get_room"
    send_message = "/send_message"
    # post_notificathion


class WSMessageBodyUserId(BaseModel):
    id: str


class WSMessageBodyRoomId(BaseModel):
    id: str


class WSMessageBodyRoomIdText(BaseModel):
    room_id: str
    text: str


class WSMessageHead(BaseModel):
    type: WSMessageType
    command: WSCommandType | None = None
    timestamp: datetime
    token: str | None = None


WSMessageBodyType = TypeVar("WSMessageBodyType")


class WSMessage(BaseModel, Generic[WSMessageBodyType]):
    head: WSMessageHead | None = None
    body: WSMessageBodyType | None = None
