import pytest
from backend.adapter.db.user_repo import UserRepo
from backend.const import POSTGRES_CONN


@pytest.fixture()
def fake_main_container(monkeypatch, async_db_connection):
    fake_main_cont = {POSTGRES_CONN: async_db_connection}
    monkeypatch.setattr('backend.adapter.db.user_repo.main_container', fake_main_cont)


async def test_user_repo_get_user(create_user, fake, fake_main_container):
    users = [
        {"username": fake.name(), "password": fake.pystr()},
        {"username": fake.name(), "password": fake.pystr()},
        {"username": fake.name(), "password": fake.pystr()},
    ]
    users_db = [await create_user(username=user['username'], password=user['password']) for user in users]
    repo = UserRepo()

    for idx, user_db in enumerate(users_db):
        res = await repo.get(user_db.username)

        assert res is not None
        assert res.username == users[idx]['username']

