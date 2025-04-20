import pytest
from backend.adapter.db.user_repo import UserRepo
from backend.const import POSTGRES_CONN


@pytest.fixture()
def fake_main_container(monkeypatch, db_session):
    fake_main_cont = {POSTGRES_CONN: db_session}
    monkeypatch.setattr('backend.adapter.db.user_repo.main_container', fake_main_cont)


async def test_user_repo_get_user(create_user, fake, fake_main_container):
    users = [
        {"login": fake.name(), "password": fake.str()},
        {"login": fake.name(), "password": fake.str()},
        {"login": fake.name(), "password": fake.str()},
    ]
    users_db = [create_user(login=user['login'], password=user['password']) for user in users]

    repo = UserRepo()

    for user_db in users_db:
        res = await repo.get(user_db.login)

        assert res is not None
        assert res.login == users[0]['login']

