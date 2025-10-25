"""Интерфейс репозитория пользователей."""

from abc import ABC, abstractmethod
from typing import List, Optional

from ...domain.user import User
from ...domain.value_objects import UserId


class UserRepository(ABC):
    """Интерфейс для работы с пользователями."""

    @abstractmethod
    async def create(self, user: User) -> User:
        """Создать пользователя."""
        pass

    @abstractmethod
    async def get_by_id(self, user_id: UserId) -> Optional[User]:
        """Получить пользователя по ID."""
        pass

    @abstractmethod
    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Получить пользователя по Telegram ID."""
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        """Обновить пользователя."""
        pass

    @abstractmethod
    async def delete(self, user_id: UserId) -> None:
        """Удалить пользователя."""
        pass

    @abstractmethod
    async def list_all(self, project_id: Optional[str] = None) -> List[User]:
        """Получить список всех пользователей."""
        pass

    @abstractmethod
    async def list_active(self, project_id: Optional[str] = None) -> List[User]:
        """Получить список активных пользователей."""
        pass

