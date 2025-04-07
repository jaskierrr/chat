from sqlalchemy import select
from sqlalchemy.orm.session import Session

from chat.adapter.db.postgres import User
from chat.const import POSTGRES_CONN
from chat.container import main_container


class UserRepo:
    def __init__(self, session: Session) -> None:
        self.session = session

    async def create(self, login, password):
        pass

    async def get(self, login) -> User:
        sql = select(User).where(User.login == login)
        result = await self.session.execute(sql)
        self.session.commit()

        return result.scalar_one()


user_repo = UserRepo(main_container[POSTGRES_CONN])

