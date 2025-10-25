"""Доменная модель пользователя."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .enums import UserRole
from .value_objects import UserId


@dataclass
class User:
    """Пользователь системы."""

    id: UserId
    telegram_id: int
    username: str
    full_name: str
    role: UserRole
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    project_id: Optional[str] = None

    def can_create_tasks(self) -> bool:
        """Проверка права на создание задач."""
        return self.role in (UserRole.OWNER, UserRole.ADMIN, UserRole.MANAGER)

    def can_manage_users(self) -> bool:
        """Проверка права на управление пользователями."""
        return self.role in (UserRole.OWNER, UserRole.ADMIN)

    def can_view_all_tasks(self) -> bool:
        """Проверка права на просмотр всех задач."""
        return self.role in (UserRole.OWNER, UserRole.ADMIN, UserRole.MANAGER)

    def can_manage_inventory(self) -> bool:
        """Проверка права на управление складом."""
        return self.role in (UserRole.OWNER, UserRole.ADMIN, UserRole.MANAGER)

    def deactivate(self) -> None:
        """Деактивация пользователя."""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        """Активация пользователя."""
        self.is_active = True
        self.updated_at = datetime.utcnow()

