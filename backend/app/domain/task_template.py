"""Доменная модель шаблона задачи."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from .enums import TaskPriority
from .value_objects import CategoryId, TaskId, UserId


@dataclass
class TaskTemplate:
    """Шаблон для создания задач."""

    id: str
    name: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    category_id: Optional[CategoryId] = None
    assignee_id: Optional[UserId] = None
    is_periodic: bool = False
    period_days: Optional[int] = None  # Периодичность в днях
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

        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("Название шаблона не может быть пустым")

        if self.is_periodic and not self.period_days:
            raise ValueError("Для периодического шаблона необходимо указать период в днях")

    def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[TaskPriority] = None,
        category_id: Optional[CategoryId] = None,
        assignee_id: Optional[UserId] = None,
    ) -> None:
        """Обновление шаблона."""
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if priority is not None:
            self.priority = priority
        if category_id is not None:
            self.category_id = category_id
        if assignee_id is not None:
            self.assignee_id = assignee_id

        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        """Деактивация шаблона."""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        """Активация шаблона."""
        self.is_active = True
        self.updated_at = datetime.utcnow()


@dataclass
class ProductSet:
    """Комплект товаров для автоматического списания."""

    id: str
    name: str
    description: Optional[str] = None
    products: dict[str, int] = field(default_factory=dict)  # product_id -> quantity
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

        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("Название комплекта не может быть пустым")

    def add_product(self, product_id: str, quantity: int) -> None:
        """Добавить товар в комплект."""
        if quantity <= 0:
            raise ValueError("Количество должно быть положительным")

        if product_id in self.products:
            self.products[product_id] += quantity
        else:
            self.products[product_id] = quantity

        self.updated_at = datetime.utcnow()

    def remove_product(self, product_id: str) -> None:
        """Удалить товар из комплекта."""
        if product_id in self.products:
            del self.products[product_id]
            self.updated_at = datetime.utcnow()

    def update_product_quantity(self, product_id: str, quantity: int) -> None:
        """Обновить количество товара в комплекте."""
        if quantity <= 0:
            raise ValueError("Количество должно быть положительным")

        if product_id not in self.products:
            raise ValueError("Товар не найден в комплекте")

        self.products[product_id] = quantity
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        """Деактивация комплекта."""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        """Активация комплекта."""
        self.is_active = True
        self.updated_at = datetime.utcnow()

