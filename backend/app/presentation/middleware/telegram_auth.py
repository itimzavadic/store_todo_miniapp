"""Middleware для авторизации через Telegram."""

from typing import Optional
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ...infrastructure.telegram_auth import validate_telegram_init_data, get_telegram_user_id
from ...config.settings import get_settings


security = HTTPBearer()


async def get_current_user(request: Request) -> Optional[int]:
    """Получить текущего пользователя из запроса.
    
    Args:
        request: HTTP запрос
        
    Returns:
        Telegram ID пользователя или None
    """
    # Получаем initData из заголовков
    init_data = request.headers.get('X-Telegram-Init-Data')
    if not init_data:
        return None
    
    # Получаем настройки
    settings = get_settings()
    
    # Проверяем подпись (для продакшена нужен bot_token)
    # В разработке пропускаем проверку
    if settings.env == "development":
        telegram_id = get_telegram_user_id(init_data)
        return telegram_id
    else:
        # В продакшене проверяем подпись
        bot_token = getattr(settings, 'telegram_bot_token', None)
        if not bot_token:
            return None
        
        if validate_telegram_init_data(init_data, bot_token):
            return get_telegram_user_id(init_data)
    
    return None


async def require_auth(request: Request) -> int:
    """Требовать авторизацию пользователя.
    
    Args:
        request: HTTP запрос
        
    Returns:
        Telegram ID пользователя
        
    Raises:
        HTTPException: Если пользователь не авторизован
    """
    telegram_id = await get_current_user(request)
    if not telegram_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Требуется авторизация через Telegram"
        )
    return telegram_id

