from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class UserLogin(BaseModel):
    username: str
    password: str

class TargetUserId(BaseModel):
    id: str

class SendMessage(BaseModel):
    user_id: UUID
    room_id: UUID
    created_at: datetime
    body: str
