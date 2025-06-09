import pytest
from sqlalchemy.orm import Session

from backend.adapter.db.postgres import User


@pytest.fixture(scope='function')
def create_user(db_session: Session, fake):
    async def factory(username, **kwargs):
        password = kwargs.get('password', fake.pystr())

        user = User(username=username, _password=password.encode())

        db_session.add(user)
        await db_session.commit()

        return user

    return factory
