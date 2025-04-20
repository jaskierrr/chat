import pytest
from sqlalchemy.orm import Session

from backend.adapter.db.postgres import User


@pytest.fixture()
async def create_user(db_session: Session, fake):
    def factory(login, **kwargs):
        password = kwargs.get('password', fake.pystr())

        user = User(login=login, _password=password)

        db_session.add(user)
        await db_session.commit()

        return user

    return factory
