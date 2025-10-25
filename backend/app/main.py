from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# Вынесение конфигурации и роутов в отдельные модули облегчает тестирование и поддержку
from .presentation.api import include_routes
from .config.settings import get_settings
from .infrastructure.database import Base, engine


def create_app() -> FastAPI:
    """Фабрика приложения для упрощения тестирования и конфигурации."""
    settings = get_settings()
    
    # Создание таблиц при старте приложения
    Base.metadata.create_all(bind=engine)
    
    app = FastAPI(
        title="Store Todo Miniapp API",
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    # Подключение статических файлов для фронтенда
    frontend_path = Path(__file__).parent.parent.parent / "frontend"
    if frontend_path.exists():
        app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")
    
    include_routes(app)
    return app


app = create_app()


