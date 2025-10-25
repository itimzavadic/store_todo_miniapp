"""Доменная модель товара."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .enums import ProductStatus
from .value_objects import Barcode, CategoryId, PhotoUrl, ProductId, Quantity


@dataclass
class Product:
    """Товар на складе."""

    id: ProductId
    name: str
    quantity: Quantity
    description: Optional[str] = None
    category_id: Optional[CategoryId] = None
    photo_url: Optional[PhotoUrl] = None
    barcode: Optional[Barcode] = None
    status: ProductStatus = ProductStatus.ACTIVE
    created_at: datetime = None
    updated_at: datetime = None
    project_id: Optional[str] = None

    def __post_init__(self):
        """Инициализация дат при создании."""
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()

        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("Название товара не может быть пустым")

    def add_quantity(self, amount: int) -> None:
        """Добавить количество товара."""
        if amount <= 0:
            raise ValueError("Количество должно быть положительным")

        new_quantity = self.quantity.value + amount
        self.quantity = Quantity(new_quantity)
        self.updated_at = datetime.utcnow()

        # Обновляем статус при добавлении
        if self.status == ProductStatus.OUT_OF_STOCK:
            self.status = ProductStatus.ACTIVE

    def subtract_quantity(self, amount: int) -> None:
        """Списать количество товара."""
        if amount <= 0:
            raise ValueError("Количество должно быть положительным")

        if self.quantity.value < amount:
            raise ValueError("Недостаточно товара на складе")

        new_quantity = self.quantity.value - amount
        self.quantity = Quantity(new_quantity)
        self.updated_at = datetime.utcnow()

        # Обновляем статус при списании
        if self.quantity.value == 0:
            self.status = ProductStatus.OUT_OF_STOCK

    def is_low_stock(self, threshold: int = 10) -> bool:
        """Проверка низкого остатка товара."""
        return self.quantity.value <= threshold and self.quantity.value > 0

    def is_out_of_stock(self) -> bool:
        """Проверка отсутствия товара."""
        return self.quantity.value == 0

    def archive(self) -> None:
        """Архивировать товар."""
        self.status = ProductStatus.ARCHIVED
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        """Активировать товар."""
        self.status = ProductStatus.ACTIVE
        self.updated_at = datetime.utcnow()

