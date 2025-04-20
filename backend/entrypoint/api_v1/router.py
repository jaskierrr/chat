from fastapi import APIRouter
from backend.entrypoint.api_v1.mem import m_router

main_router = APIRouter()

main_router.include_router(m_router)
