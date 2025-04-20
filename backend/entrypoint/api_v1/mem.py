from fastapi import (
    APIRouter,
    Cookie,
    Query,
    Response,
    WebSocket,
    WebSocketDisconnect,
    Request,
    WebSocketException,
    status,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError, NoResultFound
from asyncpg.exceptions import UniqueViolationError

from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer


from chat.adapter.db.user_repo import UserRepo
from chat.auth import auth
from chat.entrypoint.schemas.ws_schemas import WSMessage
from chat.entrypoint.schemas.request_schemas import UserLogin
import logging


logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__file__)

m_router = APIRouter()


templates = Jinja2Templates(directory="chat/templates")


# Менеджер подключений для работы с WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def router(self, message: WSMessage):
        match message:
            case True:
                pass


manager = ConnectionManager()


# @m_router.get("/", response_class=HTMLResponse)
# async def get(request: Request):
#     if async_session := main_container.get(POSTGRES_CONN):
#         async with async_session() as session:
#             result = await session.execute(select(User))
#             result = result.scalars().first()
#             print(result.login)
#
#     return templates.TemplateResponse("index.html", {"request": request})


@m_router.get("/reg", response_class=HTMLResponse)
async def send_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@m_router.get("/", response_class=HTMLResponse)
async def send_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@m_router.post("/register")
async def provide_register(user: UserLogin, request: Request):
    user_repo = UserRepo()

    try:
        await user_repo.create(user)
    except (UniqueViolationError, IntegrityError) as err:
        logger.info(f"Error occured: {err}")

        return templates.TemplateResponse(
            "register.html", {"request": request}, status_code=422
        )

    token = auth.encodeJWT(user)
    print("\ntoken", token)

    response = Response(status_code=200)
    response.set_cookie(key="token", value=token)
    response.headers["location"] = "/chat"

    return response


@m_router.post("/login")
async def provide_login(user: UserLogin, request: Request):
    # TODO сделать запрос в бд и проверить юзера
    if True:
        # print(user.username)
        user_repo = UserRepo()
        try:
            await auth.authenticate_user(user_repo, user)
        except NoResultFound as err:
            logger.error(f"Error occured: {err}")
            return templates.TemplateResponse(
                "login.html", {"request": request}, status_code=401
            )

        token = auth.encodeJWT(user)
        # logger.info("\ntoken", token)

        response = Response(status_code=200)
        response.set_cookie(key="token", value=token)
        response.headers["location"] = "/chat"

    return response


@m_router.get("/chat")
async def get(request: Request):
    cookies = request.headers.get("cookie").split(";")
    for cookie in cookies:
        if "token=" in cookie:
            token = cookie.split("=")[1]

    # TODO: переделать, писать такой try/except неправильно
    try:
        auth.decodeJWT(token)
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as err:
        logger.info("\n\nIncorrect token", err)
        return templates.TemplateResponse("login.html", {"request": request})


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "pass",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# TODO после регистрации вернуть токен
# @m_router.post("/token")
# async def login(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#     print(request.body(), 'aaa')
#
#     user_dict = fake_users_db.get(form_data.username)
#     if not user_dict:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     # user = UserInDB(**user_dict)
#     user = fake_users_db[form_data.username]
#     # hashed_password = fake_hash_password(form_data.password)
#     hashed_password = "pass"
#     if not hashed_password == user["hashed_password"]:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#
#     return {"access_token": "lol", "token_type": "bearer"}


async def get_cookie_or_token(
    websocket: WebSocket,
    session: Annotated[str | None, Cookie()] = None,
    token: Annotated[str | None, Query()] = None,
):
    if session is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


@m_router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, cookie_or_token: Annotated[str, Depends(get_cookie_or_token)]
):
    await manager.connect(websocket)

    try:
        # сменить на async
        while True:
            data = await websocket.receive_text()
            logger.info(f"Received message: {data}")
            message = WSMessage.model_validate_json(data)
            logger.info(f"Received message in class: {message}")
            # await manager.router(message)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
