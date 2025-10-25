from fastapi import FastAPI
from fastapi.routing import APIRouter

# Разделение API по модулям позволяет масштабировать проект без смешения слоёв
from .routes.health import router as health_router
from .routes.tasks import router as tasks_router
from .routes.users import router as users_router
from .routes.static import router as static_router


def include_routes(app: FastAPI) -> None:
    """Подключение всех публичных роутов приложения."""
    # Статические роуты (без префикса)
    app.include_router(static_router)
    
    # API роуты
    api_v1 = APIRouter(prefix="/api/v1")
    api_v1.include_router(health_router)
    api_v1.include_router(tasks_router)
    api_v1.include_router(users_router)
    app.include_router(api_v1)


