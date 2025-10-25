"""Value Objects для доменного слоя."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class TaskId:
    """Идентификатор задачи."""

    value: str


@dataclass(frozen=True)
class UserId:
    """Идентификатор пользователя."""

    value: str


@dataclass(frozen=True)
class ProductId:
    """Идентификатор товара."""

    value: str


@dataclass(frozen=True)
class CategoryId:
    """Идентификатор категории."""

    value: str


@dataclass(frozen=True)
class PhotoUrl:
    """URL фотографии."""

    value: str

    def __post_init__(self):
        """Валидация URL фотографии."""
        if not self.value:
            raise ValueError("URL фотографии не может быть пустым")


@dataclass(frozen=True)
class Barcode:
    """Штрих-код товара."""

    value: str

    def __post_init__(self):
        """Валидация штрих-кода."""
        if not self.value:
            raise ValueError("Штрих-код не может быть пустым")


@dataclass(frozen=True)
class Quantity:
    """Количество товара."""

    value: int

    def __post_init__(self):
        """Валидация количества."""
        if self.value < 0:
            raise ValueError("Количество не может быть отрицательным")


@dataclass(frozen=True)
class Deadline:
    """Срок выполнения задачи."""

    value: datetime

    def __post_init__(self):
        """Валидация срока."""
        if not self.value:
            raise ValueError("Срок выполнения обязателен")


@dataclass(frozen=True)
class Comment:
    """Комментарий к задаче."""

    value: str

    def __post_init__(self):
        """Валидация комментария."""
        if not self.value or len(self.value.strip()) == 0:
            raise ValueError("Комментарий не может быть пустым")

