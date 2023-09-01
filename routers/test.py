from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/health-check")
async def health_check_routes():
    """
    서버 헬스 체크 합니다.
    """
    return "FastAPI-01 alive version v1.3.1"

@router.get("/")
async def header_routes():
    """
    기본 페이지 라우팅
    """
    file_path = os.path.join(".", "headingPage.html")
    return FileResponse(file_path)