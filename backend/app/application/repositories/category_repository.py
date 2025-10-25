"""Интерфейс репозитория категорий."""

from abc import ABC, abstractmethod
from typing import List, Optional

from ...domain.category import Category
from ...domain.value_objects import CategoryId


class CategoryRepository(ABC):
    """Интерфейс для работы с категориями."""

    @abstractmethod
    async def create(self, category: Category) -> Category:
        """Создать категорию."""
        pass

    @abstractmethod
    async def get_by_id(self, category_id: CategoryId) -> Optional[Category]:
        """Получить категорию по ID."""
        pass

    @abstractmethod
    async def update(self, category: Category) -> Category:
        """Обновить категорию."""
        pass

    @abstractmethod
    async def delete(self, category_id: CategoryId) -> None:
        """Удалить категорию."""
        pass

    @abstractmethod
    async def list_all(self, project_id: Optional[str] = None) -> List[Category]:
        """Получить список всех категорий."""
        pass

    @abstractmethod
    async def list_active(self, project_id: Optional[str] = None) -> List[Category]:
        """Получить список активных категорий."""
        pass

