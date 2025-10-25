"""Пакет доменной модели: сущности и бизнес-правила."""

from .category import Category
from .enums import ProductStatus, TaskPriority, TaskStatus, UserRole
from .product import Product
from .task import Task
from .task_template import ProductSet, TaskTemplate
from .user import User
from .value_objects import (
    Barcode,
    CategoryId,
    Comment,
    Deadline,
    PhotoUrl,
    ProductId,
    Quantity,
    TaskId,
    UserId,
)

__all__ = [
    # Enums
    "TaskStatus",
    "TaskPriority",
    "UserRole",
    "ProductStatus",
    # Value Objects
    "TaskId",
    "UserId",
    "ProductId",
    "CategoryId",
    "PhotoUrl",
    "Barcode",
    "Quantity",
    "Deadline",
    "Comment",
    # Entities
    "User",
    "Task",
    "Product",
    "Category",
    "TaskTemplate",
    "ProductSet",
]

