from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import (
    UUID,
    DateTime,
    ForeignKey,
    LargeBinary,
    Table,
    Column,
    String,
    func,
)
import uuid
import asyncio
from hashlib import pbkdf2_hmac

from config import config


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
        server_default=func.gen_random_uuid()
    )
    login: Mapped[str] = mapped_column(String(50))
    password: Mapped[bytes] = mapped_column(LargeBinary)

    @hybrid_property
    def password_(self):
        """Return the hashed user password."""
        return self.password

    @password.setter
    async def password_(self, new_pass):
        """Salt/Hash and save the user's new password."""
        loop = asyncio.get_event_loop()

        new_password_hash = await loop.run_in_executor(
            None, compute_new_password_hash, new_pass, config.config.password.salt
        )
        # new_password_hash = compute_new_password_hash(new_pass, self._salt)
        self.password = new_password_hash


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), comment="Room ID", primary_key=True
    )
    name: Mapped[str] = mapped_column(String(100))


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), comment="Room ID", primary_key=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    body: Mapped[str] = mapped_column(String(500), nullable=False)


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
