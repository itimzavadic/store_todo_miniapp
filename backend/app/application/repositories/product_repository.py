"""Интерфейс репозитория товаров."""

from abc import ABC, abstractmethod
from typing import List, Optional

from ...domain.product import Product
from ...domain.value_objects import ProductId


class ProductRepository(ABC):
    """Интерфейс для работы с товарами."""

    @abstractmethod
    async def create(self, product: Product) -> Product:
        """Создать товар."""
        pass

    @abstractmethod
    async def get_by_id(self, product_id: ProductId) -> Optional[Product]:
        """Получить товар по ID."""
        pass

    @abstractmethod
    async def update(self, product: Product) -> Product:
        """Обновить товар."""
        pass

    @abstractmethod
    async def delete(self, product_id: ProductId) -> None:
        """Удалить товар."""
        pass

    @abstractmethod
    async def list_all(self, project_id: Optional[str] = None) -> List[Product]:
        """Получить список всех товаров."""
        pass

    @abstractmethod
    async def list_low_stock(self, threshold: int = 10, project_id: Optional[str] = None) -> List[Product]:
        """Получить список товаров с низким остатком."""
        pass

    @abstractmethod
    async def list_out_of_stock(self, project_id: Optional[str] = None) -> List[Product]:
        """Получить список товаров, которых нет в наличии."""
        pass

    @abstractmethod
    async def search_by_name(self, name: str, project_id: Optional[str] = None) -> List[Product]:
        """Поиск товаров по названию."""
        pass

    @abstractmethod
    async def get_by_barcode(self, barcode: str, project_id: Optional[str] = None) -> Optional[Product]:
        """Получить товар по штрих-коду."""
        pass

