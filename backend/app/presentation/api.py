from fastapi import FastAPI
from fastapi.routing import APIRouter

# Разделение API по модулям позволяет масштабировать проект без смешения слоёв
from .routes.health import router as health_router


def include_routes(app: FastAPI) -> None:
    """Подключение всех публичных роутов приложения."""
    api_v1 = APIRouter(prefix="/api/v1")
    api_v1.include_router(health_router)
    app.include_router(api_v1)


