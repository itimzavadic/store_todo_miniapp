"""Реализация репозитория пользователей."""

from typing import List, Optional

from sqlalchemy.orm import Session

from ...application.repositories.user_repository import UserRepository
from ...domain.user import User
from ...domain.value_objects import UserId
from ...domain.enums import UserRole
from ..models import UserModel


class UserRepositoryImpl(UserRepository):
    """Реализация репозитория пользователей."""

    def __init__(self, db: Session):
        self.db = db

    async def create(self, user: User) -> User:
        """Создать пользователя."""
        user_model = UserModel(
            id=user.id.value,
            telegram_id=user.telegram_id,
            username=user.username,
            full_name=user.full_name,
            role=user.role.value,
            is_active=user.is_active,
            project_id=user.project_id,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        self.db.add(user_model)
        self.db.commit()
        self.db.refresh(user_model)
        return self._to_domain(user_model)

    async def get_by_id(self, user_id: UserId) -> Optional[User]:
        """Получить пользователя по ID."""
        user_model = self.db.query(UserModel).filter(UserModel.id == user_id.value).first()
        return self._to_domain(user_model) if user_model else None

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Получить пользователя по Telegram ID."""
        user_model = self.db.query(UserModel).filter(UserModel.telegram_id == telegram_id).first()
        return self._to_domain(user_model) if user_model else None

    async def update(self, user: User) -> User:
        """Обновить пользователя."""
        user_model = self.db.query(UserModel).filter(UserModel.id == user.id.value).first()
        if not user_model:
            raise ValueError("Пользователь не найден")

        user_model.username = user.username
        user_model.full_name = user.full_name
        user_model.role = user.role.value
        user_model.is_active = user.is_active
        user_model.project_id = user.project_id
        user_model.updated_at = user.updated_at

        self.db.commit()
        self.db.refresh(user_model)
        return self._to_domain(user_model)

    async def delete(self, user_id: UserId) -> None:
        """Удалить пользователя."""
        user_model = self.db.query(UserModel).filter(UserModel.id == user_id.value).first()
        if user_model:
            self.db.delete(user_model)
            self.db.commit()

    async def list_all(self, project_id: Optional[str] = None) -> List[User]:
        """Получить список всех пользователей."""
        query = self.db.query(UserModel)
        if project_id:
            query = query.filter(UserModel.project_id == project_id)
        user_models = query.all()
        return [self._to_domain(model) for model in user_models]

    async def list_active(self, project_id: Optional[str] = None) -> List[User]:
        """Получить список активных пользователей."""
        query = self.db.query(UserModel).filter(UserModel.is_active == True)
        if project_id:
            query = query.filter(UserModel.project_id == project_id)
        user_models = query.all()
        return [self._to_domain(model) for model in user_models]

    def _to_domain(self, model: UserModel) -> User:
        """Преобразовать модель БД в доменную сущность."""
        if not model:
            return None

        return User(
            id=UserId(value=model.id),
            telegram_id=model.telegram_id,
            username=model.username,
            full_name=model.full_name,
            role=UserRole(model.role),
            is_active=model.is_active,
            project_id=model.project_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

