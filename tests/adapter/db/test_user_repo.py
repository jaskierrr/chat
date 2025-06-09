from backend.adapter.db.user_repo import UserRepo


async def test_user_repo_get_user(create_user, fake, fake_main_container):
    users = [
        {"username": fake.name(), "password": fake.pystr()},
        {"username": fake.name(), "password": fake.pystr()},
        {"username": fake.name(), "password": fake.pystr()},
    ]
    users_db = [
        await create_user(username=user["username"], password=user["password"])
        for user in users
    ]
    repo = UserRepo()

    for idx, user_db in enumerate(users_db):
        res = await repo.get(user_db.username)

        assert res is not None
        assert res.username == users[idx]["username"]
