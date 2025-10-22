from fastapi import FastAPI

# Вынесение конфигурации и роутов в отдельные модули облегчает тестирование и поддержку
from .presentation.api import include_routes
from .config.settings import get_settings


def create_app() -> FastAPI:
    """Фабрика приложения для упрощения тестирования и конфигурации."""
    settings = get_settings()
    app = FastAPI(
        title="Store Todo Miniapp API",
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
    )
    include_routes(app)
    return app


app = create_app()


