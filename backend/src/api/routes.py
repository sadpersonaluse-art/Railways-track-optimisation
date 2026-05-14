from fastapi import APIRouter
from .endpoints import info

api_router = APIRouter()

api_router.include_router(info.router)
