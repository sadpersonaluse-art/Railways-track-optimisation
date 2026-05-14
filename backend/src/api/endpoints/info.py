from fastapi import APIRouter
from pydantic import BaseModel


class InfoResponse(BaseModel):
    project: str
    status: str
    version: str


router = APIRouter()


@router.get("/info", response_model=InfoResponse)
async def get_info():
    return {
        "project": "Railways Track Optimisation",
        "status": "development",
        "version": "1.0"
    }
