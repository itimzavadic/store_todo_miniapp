"""Утилиты для авторизации через Telegram."""

import hashlib
import hmac
from typing import Optional, Dict
from urllib.parse import parse_qsl, urlencode


def validate_telegram_init_data(init_data: str, bot_token: str) -> bool:
    """Проверка подписи Telegram initData.
    
    Args:
        init_data: Строка с данными от Telegram
        bot_token: Токен бота от Telegram
        
    Returns:
        True если подпись валидна
    """
    try:
        # Парсим данные
        parsed_data = dict(parse_qsl(init_data))
        
        # Извлекаем hash и остальные данные
        hash_value = parsed_data.pop('hash', None)
        if not hash_value:
            return False
        
        # Сортируем данные по ключу
        data_check_string = '\n'.join(f"{k}={v}" for k, v in sorted(parsed_data.items()))
        
        # Создаем секретный ключ
        secret_key = hmac.new(
            b"WebAppData",
            bot_token.encode(),
            hashlib.sha256
        ).digest()
        
        # Проверяем подпись
        calculated_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return calculated_hash == hash_value
    except Exception:
        return False


def parse_telegram_user(init_data: str) -> Optional[Dict]:
    """Извлечение данных пользователя из initData.
    
    Args:
        init_data: Строка с данными от Telegram
        
    Returns:
        Словарь с данными пользователя или None
    """
    try:
        parsed_data = dict(parse_qsl(init_data))
        user_data = parsed_data.get('user')
        if not user_data:
            return None
        
        # Парсим JSON данные пользователя
        import json
        user = json.loads(user_data)
        return user
    except Exception:
        return None


def get_telegram_user_id(init_data: str) -> Optional[int]:
    """Получить Telegram ID пользователя из initData.
    
    Args:
        init_data: Строка с данными от Telegram
        
    Returns:
        Telegram ID пользователя или None
    """
    user = parse_telegram_user(init_data)
    if user:
        return user.get('id')
    return None

