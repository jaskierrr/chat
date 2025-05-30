import json
from logging import basicConfig, getLevelName, getLogger
from typing import Annotated, Any

from asyncpg.exceptions import UniqueViolationError
from fastapi import (
    APIRouter,
    Depends,
    Query,
    Request,
    Response,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
    status,
)
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError, NoResultFound

from backend.adapter.db.user_repo import UserRepo
from backend.auth import auth
from backend.config import config
from backend.entrypoints.schemas.request_schemas import UserLogin
from backend.entrypoints.schemas.ws_schemas import (
    WSEventType,
    WSMessage,
)
from backend.services.auth import AuthService
from backend.services.login import LoginService
from backend.services.ws import WSService

basicConfig(format="%(levelname)s: %(message)s", level=getLevelName(config.log_level))
logger = getLogger(__file__)

m_router = APIRouter()

auth_service = AuthService()
login_service = LoginService()
ws_servise = WSService()

# templates = Jinja2Templates(directory="backend/templates")
templates = Jinja2Templates(directory="templates")


# Менеджер подключений для работы с WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        self.active_connections.pop(user_id, None)

    async def broadcast(self, message: str):
        for user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)

    async def send_message(self, user_id: str, message: WSMessage):
        await self.active_connections[user_id].send_text(message)

    async def router(self, user_id: str, message: dict[str, Any]):
        print(message)
        try:
            match message["head"]["event"]:
                case WSEventType.get_rooms_list.value:
                    response_msg = await ws_servise.get_rooms_list(user_id, message)
                case WSEventType.get_room.value:
                    response_msg = await ws_servise.get_room(message)
                case WSEventType.get_users_list.value:
                    response_msg = await ws_servise.get_users_list(message)
                case WSEventType.send_message.value:
                    response_msg = await ws_servise.send_message(user_id, message)
                case WSEventType.create_room.value:
                    response_msg = await ws_servise.create_room(message)
        except Exception as e:
            logger.exception(f"Cant provide WS respone: {e}")
            return

        res = response_msg.model_dump_json()
        await self.send_message(user_id, res)
        logger.info("msg sent %s, %s", self.active_connections.keys(), user_id)


manager = ConnectionManager()


async def get_token(
    websocket: WebSocket,
    token: Annotated[str | None, Query()] = None,
):
    # print('lol')
    if token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return token


@m_router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, cookie_or_token: Annotated[str, Depends(get_token)]
):
    # print(f'{cookie_or_token=}')
    user_id = auth.decodeJWT(cookie_or_token)["user_id"]
    await manager.connect(websocket, user_id)

    try:
        # сменить на async
        while True:
            data = await websocket.receive_text()
            print(data)
            data = json.loads(data)
            await manager.router(user_id, data)
    except WebSocketDisconnect:
        user_id = auth.decodeJWT(cookie_or_token)["user_id"]
        manager.disconnect(user_id)


@m_router.get("/", response_class=HTMLResponse)
async def send_login_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@m_router.post("/token")
async def validate_token(request: Request):
    token_payload = auth_service.validate_token(request)
    try:
        user_id = {"id": token_payload["user_id"]}
        return JSONResponse(content=user_id, status_code=200)
    except Exception:
        return Response(status_code=404)


@m_router.post("/login")
async def provide_login(user_data: UserLogin, user_repo: UserRepo = Depends(UserRepo)):
    try:
        user = await login_service.login_user(user_data, user_repo)
    except NoResultFound as err:
        logger.error(f"Error occured: {err}")

        response = JSONResponse(
            content={"error": f"user not found: {err}"}, status_code=404
        )
        return response

    token = auth.encodeJWT(user)
    print("\ntoken", token)

    # user_id = {"id": str(user.id)}
    # res = UserResponse(**user.dict(exclude={'password'}))
    # data = user.__dict__.copy()
    # data.pop('_sa_instance_state', None)
    # data.pop('_password', None)
    # res = UserResponse(**data)
    res = {'username': str(user.username), 'id': str(user.id)}

    print("user", res)

    response = JSONResponse(content=res, status_code=200)
    response.set_cookie(key="token", value=token)

    return response


@m_router.get("/reg", response_class=HTMLResponse)
async def send_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


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
    # response.headers["location"] = "/chat"

    return response
