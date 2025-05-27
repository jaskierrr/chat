from uuid import UUID
from pydantic import BaseModel, ConfigDict
from backend.adapter.db.postgres import Room, User


class UserResponse(BaseModel):
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


class WSMessageBodyGetRoom(BaseModel):
    pass

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

