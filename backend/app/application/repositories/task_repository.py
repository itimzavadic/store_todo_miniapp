"""Интерфейс репозитория задач."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from ...domain.task import Task
from ...domain.value_objects import TaskId, UserId


class TaskRepository(ABC):
    """Интерфейс для работы с задачами."""

    @abstractmethod
    async def create(self, task: Task) -> Task:
        """Создать задачу."""
        pass

    @abstractmethod
    async def get_by_id(self, task_id: TaskId) -> Optional[Task]:
        """Получить задачу по ID."""
        pass

    @abstractmethod
    async def update(self, task: Task) -> Task:
        """Обновить задачу."""
        pass

    @abstractmethod
    async def delete(self, task_id: TaskId) -> None:
        """Удалить задачу."""
        pass

    @abstractmethod
    async def list_by_assignee(
        self, assignee_id: UserId, project_id: Optional[str] = None
    ) -> List[Task]:
        """Получить список задач по исполнителю."""
        pass

    @abstractmethod
    async def list_by_creator(
        self, creator_id: UserId, project_id: Optional[str] = None
    ) -> List[Task]:
        """Получить список задач по создателю."""
        pass

    @abstractmethod
    async def list_by_project(self, project_id: str) -> List[Task]:
        """Получить список всех задач проекта."""
        pass

    @abstractmethod
    async def list_overdue(self, project_id: Optional[str] = None) -> List[Task]:
        """Получить список просроченных задач."""
        pass

    @abstractmethod
    async def list_by_date_range(
        self, start_date: datetime, end_date: datetime, project_id: Optional[str] = None
    ) -> List[Task]:
        """Получить список задач в диапазоне дат."""
        pass

