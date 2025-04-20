from datetime import datetime
from pydantic import BaseModel
from enum import StrEnum


class WSMessageType(StrEnum):
    command = "command"
    message = "message"


class WSCommandType(StrEnum):
    get_rooms_list = "/get_rooms_list"
    get_room = "/get_room"
    # post_notificathion


class WSMessageBody(BaseModel):
    text: str | None = None


class WSMessageHead(BaseModel):
    type: WSMessageType
    command: WSCommandType | None = None
    timestamp: datetime
    token: str


class WSMessage(BaseModel):
    head: WSMessageHead | None = None
    body: WSMessageBody | None = None
