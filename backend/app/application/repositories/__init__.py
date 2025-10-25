"""Интерфейсы репозиториев (порты)."""

from .category_repository import CategoryRepository
from .product_repository import ProductRepository
from .task_repository import TaskRepository
from .user_repository import UserRepository

__all__ = [
    "UserRepository",
    "TaskRepository",
    "ProductRepository",
    "CategoryRepository",
]

