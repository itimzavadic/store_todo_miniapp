"""Pydantic схемы для задач."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from ...domain.enums import TaskPriority, TaskStatus


class TaskPriorityEnum(str):
    """Enum для приоритета задачи в Pydantic схеме."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskStatusEnum(str):
    """Enum для статуса задачи в Pydantic схеме."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class TaskBase(BaseModel):
    """Базовая схема задачи."""

    title: str = Field(..., min_length=1, max_length=200, description="Название задачи")
    description: Optional[str] = Field(None, description="Описание задачи")
    priority: str = Field("medium", description="Приоритет задачи")
    category_id: Optional[str] = Field(None, description="ID категории")
    assignee_id: Optional[str] = Field(None, description="ID исполнителя")
    deadline: Optional[datetime] = Field(None, description="Срок выполнения")


class TaskCreate(TaskBase):
    """Схема для создания задачи."""

    pass


class TaskUpdate(BaseModel):
    """Схема для обновления задачи."""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Optional[str] = None
    category_id: Optional[str] = None
    assignee_id: Optional[str] = None
    deadline: Optional[datetime] = None


class TaskComplete(BaseModel):
    """Схема для выполнения задачи."""

    comment: Optional[str] = Field(None, description="Комментарий к выполнению")
    photos: Optional[List[str]] = Field(None, description="URL фотографий")


class TaskResponse(TaskBase):
    """Схема ответа с задачей."""

    id: str
    status: str
    creator_id: str
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    completion_photos: Optional[List[str]] = None
    completion_comment: Optional[str] = None
    project_id: Optional[str] = None

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """Схема списка задач."""

    tasks: List[TaskResponse]
    total: int

