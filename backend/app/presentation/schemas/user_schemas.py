"""Pydantic схемы для пользователей."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from ...domain.enums import UserRole


class UserRoleEnum(str):
    """Enum для роли пользователя в Pydantic схеме."""
    OWNER = "owner"
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"


class UserBase(BaseModel):
    """Базовая схема пользователя."""

    telegram_id: int = Field(..., description="Telegram ID пользователя")
    username: str = Field(..., min_length=1, max_length=100, description="Имя пользователя")
    full_name: str = Field(..., min_length=1, max_length=200, description="Полное имя")
    role: str = Field("employee", description="Роль пользователя")


class UserCreate(UserBase):
    """Схема для создания пользователя."""

    project_id: Optional[str] = Field(None, description="ID проекта")


class UserUpdate(BaseModel):
    """Схема для обновления пользователя."""

    username: Optional[str] = Field(None, min_length=1, max_length=100)
    full_name: Optional[str] = Field(None, min_length=1, max_length=200)
    role: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """Схема ответа с пользователем."""

    id: str
    is_active: bool
    project_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """Схема списка пользователей."""

    users: List[UserResponse]
    total: int

