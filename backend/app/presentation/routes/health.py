from fastapi import APIRouter

# Healthcheck выносится отдельно, чтобы быть доступным всегда и без лишних зависимостей
router = APIRouter(tags=["health"])


@router.get("/health")
async def healthcheck() -> dict:
    """Проверка готовности сервиса.

    Возвращаем минимальную диагностическую информацию, пригодную для мониторинга.
    """
    return {"status": "ok"}


