"""Use cases для работы с пользователями."""

from typing import List, Optional

from ...domain.user import User
from ...domain.enums import UserRole
from ...domain.value_objects import UserId
from ..repositories import UserRepository


class CreateUserUseCase:
    """Use case для создания пользователя."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(
        self,
        telegram_id: int,
        username: str,
        full_name: str,
        role: str,
        project_id: Optional[str] = None,
    ) -> User:
        """Создать нового пользователя."""
        # Проверка существования пользователя с таким Telegram ID
        existing_user = await self.user_repository.get_by_telegram_id(telegram_id)
        if existing_user:
            raise ValueError("Пользователь с таким Telegram ID уже существует")

        from datetime import datetime

        user = User(
            id=UserId(value=str(telegram_id)),
            telegram_id=telegram_id,
            username=username,
            full_name=full_name,
            role=UserRole(role),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            is_active=True,
            project_id=project_id,
        )

        return await self.user_repository.create(user)


class GetUserUseCase:
    """Use case для получения пользователя."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: UserId) -> Optional[User]:
        """Получить пользователя по ID."""
        return await self.user_repository.get_by_id(user_id)

    async def execute_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Получить пользователя по Telegram ID."""
        return await self.user_repository.get_by_telegram_id(telegram_id)


class ListUsersUseCase:
    """Use case для получения списка пользователей."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, project_id: Optional[str] = None, active_only: bool = False) -> List[User]:
        """Получить список пользователей."""
        if active_only:
            return await self.user_repository.list_active(project_id)
        return await self.user_repository.list_all(project_id)

