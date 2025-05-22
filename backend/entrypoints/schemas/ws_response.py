from uuid import UUID
from pydantic import BaseModel, ConfigDict
from backend.adapter.db.postgres import Room


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
