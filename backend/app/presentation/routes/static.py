"""Роут для отдачи статического HTML."""

from fastapi import APIRouter
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter()


@router.get("/")
async def index():
    """Главная страница Mini App."""
    frontend_path = Path(__file__).parent.parent.parent.parent / "frontend" / "index.html"
    if frontend_path.exists():
        return FileResponse(str(frontend_path))
    return {"message": "Frontend not found"}

