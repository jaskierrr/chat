
import json

from backend.adapter.db.user_repo import UserRepo
from backend.entrypoints.api_v1.mem import provide_login


async def test_login_service(create_user, fake, fake_main_container):
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

    for user in users_db:
        response = await provide_login(user, repo)

        assert response.status_code == 200

        response_body = json.loads(response.body.decode('utf-8'))
        assert response_body.get('username') == user.username



    # for idx, user_db in enumerate(users_db):
    #     res = await repo.get(user_db.username)
    #     print(user_db.password)
    #
    #     assert res is not None
    #     assert res.username == users[idx]["username"]
