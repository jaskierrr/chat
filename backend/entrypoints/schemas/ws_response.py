from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from backend.adapter.db.postgres import Message, Room, User


class UsersSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str


class RoomSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str


class WSMessageBodyGetRoomsList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    rooms: list[RoomSchema]

    @classmethod
    def unpack_rooms(cls, rooms_db: list[Room]) -> "WSMessageBodyGetRoomsList":
        return WSMessageBodyGetRoomsList(
            rooms=[RoomSchema.model_validate(room) for room in rooms_db]
        )


class MessagesSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    text: str
    created_at: datetime
    user: UsersSchema
    room: RoomSchema


class WSMessageBodyGetRoom(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    room: RoomSchema | None
    messages: list[MessagesSchema]

    @classmethod
    def unpack_messages(cls, messages_db: list[Message], rooms_db) -> "WSMessageBodyGetRoom":
        print([message for message in messages_db])
        return WSMessageBodyGetRoom(
            messages=[MessagesSchema.model_validate(message) for message in messages_db],
            room=RoomSchema.model_validate(rooms_db)
        )

class UsersSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str


class WSMessageBodyGetUsersList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    users: list[UsersSchema]

    @classmethod
    def unpack_users(cls, users_db: list[User]) -> "WSMessageBodyGetUsersList":
        return WSMessageBodyGetUsersList(
            users=[UsersSchema.model_validate(user) for user in users_db]
        )

