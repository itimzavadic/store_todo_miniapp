"""Доменная модель задачи."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from .enums import TaskPriority, TaskStatus
from .value_objects import CategoryId, Comment, Deadline, PhotoUrl, TaskId, UserId


@dataclass
class Task:
    """Задача для выполнения."""

    id: TaskId
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    category_id: Optional[CategoryId]
    assignee_id: Optional[UserId]  # Исполнитель
    creator_id: UserId  # Создатель
    deadline: Optional[Deadline]
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    completion_photos: List[PhotoUrl] = field(default_factory=list)
    completion_comment: Optional[Comment] = None
    project_id: Optional[str] = None

    def __post_init__(self):
        """Валидация задачи."""
        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("Название задачи не может быть пустым")

    def mark_as_completed(self, comment: Optional[str] = None, photos: Optional[List[str]] = None) -> None:
        """Отметить задачу как выполненную."""
        if self.status == TaskStatus.COMPLETED:
            raise ValueError("Задача уже выполнена")

        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

        if comment:
            self.completion_comment = Comment(comment)

        if photos:
            self.completion_photos = [PhotoUrl(photo) for photo in photos]

    def mark_as_in_progress(self) -> None:
        """Отметить задачу как выполняемую."""
        if self.status == TaskStatus.COMPLETED:
            raise ValueError("Выполненную задачу нельзя вернуть в работу")

        self.status = TaskStatus.IN_PROGRESS
        self.updated_at = datetime.utcnow()

    def archive(self) -> None:
        """Архивировать задачу."""
        self.status = TaskStatus.ARCHIVED
        self.updated_at = datetime.utcnow()

    def restore_from_archive(self) -> None:
        """Восстановить задачу из архива."""
        if self.status != TaskStatus.ARCHIVED:
            raise ValueError("Можно восстановить только архивированные задачи")

        self.status = TaskStatus.PENDING
        self.updated_at = datetime.utcnow()

    def update_assignee(self, assignee_id: UserId) -> None:
        """Обновить исполнителя задачи."""
        self.assignee_id = assignee_id
        self.updated_at = datetime.utcnow()

    def update_deadline(self, deadline: Deadline) -> None:
        """Обновить срок выполнения."""
        self.deadline = deadline
        self.updated_at = datetime.utcnow()

    def is_overdue(self) -> bool:
        """Проверка просроченности задачи."""
        if not self.deadline or self.status == TaskStatus.COMPLETED:
            return False
        return datetime.utcnow() > self.deadline.value

    def update_priority(self, priority: TaskPriority) -> None:
        """Обновить приоритет задачи."""
        self.priority = priority
        self.updated_at = datetime.utcnow()

