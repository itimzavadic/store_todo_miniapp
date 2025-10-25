"""Перечисления для доменного слоя."""

from enum import Enum


class TaskStatus(str, Enum):
    """Статус задачи."""

    PENDING = "pending"  # В ожидании
    IN_PROGRESS = "in_progress"  # В работе
    COMPLETED = "completed"  # Выполнена
    ARCHIVED = "archived"  # Архивирована


class TaskPriority(str, Enum):
    """Приоритет задачи."""

    LOW = "low"  # Низкий
    MEDIUM = "medium"  # Средний
    HIGH = "high"  # Высокий
    URGENT = "urgent"  # Срочный


class UserRole(str, Enum):
    """Роль пользователя."""

    OWNER = "owner"  # Владелец
    ADMIN = "admin"  # Администратор
    MANAGER = "manager"  # Менеджер
    EMPLOYEE = "employee"  # Сотрудник


class ProductStatus(str, Enum):
    """Статус товара."""

    ACTIVE = "active"  # Активен
    OUT_OF_STOCK = "out_of_stock"  # Нет в наличии
    ARCHIVED = "archived"  # Архивирован

