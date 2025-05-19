from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import (
    UUID,
    DateTime,
    ForeignKey,
    LargeBinary,
    Table,
    Column,
    String,
)
import uuid
from hashlib import pbkdf2_hmac

from backend.config import config


class Base(DeclarativeBase):
    pass


user_room = Table(
    "user_room",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("room_id", UUID(as_uuid=True), ForeignKey("rooms.id"), primary_key=True),
)


def compute_new_password_hash(password: str, salt: str):
    iterations = 100

    return pbkdf2_hmac("sha512", password.encode(), salt.encode(), iterations)


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        comment="User ID",
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
    )
    login: Mapped[str] = mapped_column(String(50), unique=True)
    _password: Mapped[bytes] = mapped_column(LargeBinary, name="password")

    @hybrid_property
    def password(self):
        """Return the hashed user password."""
        return self._password

    @password.setter
    def password(self, new_pass):
        """Salt/Hash and save the user's new password."""
        new_password_hash = compute_new_password_hash(new_pass, config.password.salt)
        self._password = new_password_hash

    messages: Mapped[list["Message"]] = relationship(back_populates="user")


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        comment="Room ID",
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
    )
    name: Mapped[str] = mapped_column(String(100))

    messages: Mapped[list["Message"]] = relationship(back_populates="room")

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        comment="Message ID",
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        comment="User ID",
    )
    room_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("rooms.id"),
        comment="Room ID",
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    body: Mapped[str] = mapped_column(String(500), nullable=False)

    room: Mapped[Room] = relationship(back_populates="messages")
    user: Mapped[User] = relationship(back_populates="messages")


#
# def ping_bd():
#     engine = create_engine(config.db.dsn.unicode_string())
#
#     try:
#         # Устанавливаем соединение
#         connection = engine.connect()
#
#         query = text("SELECT 1")
#         result = connection.execute(query)
#
#         if result.fetchone()[0] == 1:
#             print("Подключение успешно, база данных отвечает")
#         else:
#             print("Неожиданный ответ от базы данных")
#
#         Base.metadata.create_all(engine)
#
#         insertUser = insert(User).values(id=UUID(int=123), login='ivan', password=b'aaa')
#         print(insertUser)
#         result = connection.execute(insertUser)
#         print(result)
#
#         # Закрываем соединение
#         connection.close()
#     except Exception as e:
#         print("Ошибка подключения или выполнения запроса:", e)
