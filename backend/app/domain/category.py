"""Доменная модель категории."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .value_objects import CategoryId


@dataclass
class Category:
    """Категория для задач и товаров."""

    id: CategoryId
    name: str
    description: Optional[str] = None
    color: Optional[str] = None  # Цвет для визуального выделения
    created_at: datetime = None
    updated_at: datetime = None
    is_active: bool = True
    project_id: Optional[str] = None

    def __post_init__(self):
        """Инициализация дат при создании."""
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()

    def update(self, name: Optional[str] = None, description: Optional[str] = None, color: Optional[str] = None) -> None:
        """Обновление категории."""
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if color is not None:
            self.color = color
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        """Деактивация категории."""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        """Активация категории."""
        self.is_active = True
        self.updated_at = datetime.utcnow()

