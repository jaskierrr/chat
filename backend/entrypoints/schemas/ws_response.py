from uuid import UUID
from pydantic import BaseModel, ConfigDict

from backend.adapter.db.postgres import Room


class RoomSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str


class WSMessageBodyGetRooms(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    rooms: list[RoomSchema]

    @classmethod
    def unpack_rooms(cls, rooms_db: list[Room]) -> "WSMessageBodyGetRooms":
        return WSMessageBodyGetRooms(
            rooms=[RoomSchema.model_validate(room) for room in rooms_db]
        )

