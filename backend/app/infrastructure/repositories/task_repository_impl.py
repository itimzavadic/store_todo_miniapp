"""Реализация репозитория задач."""

from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from ...application.repositories.task_repository import TaskRepository
from ...domain.task import Task
from ...domain.value_objects import TaskId, UserId
from ...domain.enums import TaskStatus, TaskPriority
from ..models import TaskModel


class TaskRepositoryImpl(TaskRepository):
    """Реализация репозитория задач."""

    def __init__(self, db: Session):
        self.db = db

    async def create(self, task: Task) -> Task:
        """Создать задачу."""
        task_model = TaskModel(
            id=task.id.value,
            title=task.title,
            description=task.description,
            status=task.status.value,
            priority=task.priority.value,
            category_id=task.category_id.value if task.category_id else None,
            assignee_id=task.assignee_id.value if task.assignee_id else None,
            creator_id=task.creator_id.value,
            deadline=task.deadline.value if task.deadline else None,
            completed_at=task.completed_at,
            completion_photos=[photo.value for photo in task.completion_photos] if task.completion_photos else None,
            completion_comment=task.completion_comment.value if task.completion_comment else None,
            project_id=task.project_id,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )
        self.db.add(task_model)
        self.db.commit()
        self.db.refresh(task_model)
        return self._to_domain(task_model)

    async def get_by_id(self, task_id: TaskId) -> Optional[Task]:
        """Получить задачу по ID."""
        task_model = self.db.query(TaskModel).filter(TaskModel.id == task_id.value).first()
        return self._to_domain(task_model) if task_model else None

    async def update(self, task: Task) -> Task:
        """Обновить задачу."""
        task_model = self.db.query(TaskModel).filter(TaskModel.id == task.id.value).first()
        if not task_model:
            raise ValueError("Задача не найдена")

        task_model.title = task.title
        task_model.description = task.description
        task_model.status = task.status.value
        task_model.priority = task.priority.value
        task_model.category_id = task.category_id.value if task.category_id else None
        task_model.assignee_id = task.assignee_id.value if task.assignee_id else None
        task_model.deadline = task.deadline.value if task.deadline else None
        task_model.completed_at = task.completed_at
        task_model.completion_photos = [photo.value for photo in task.completion_photos] if task.completion_photos else None
        task_model.completion_comment = task.completion_comment.value if task.completion_comment else None
        task_model.updated_at = task.updated_at

        self.db.commit()
        self.db.refresh(task_model)
        return self._to_domain(task_model)

    async def delete(self, task_id: TaskId) -> None:
        """Удалить задачу."""
        task_model = self.db.query(TaskModel).filter(TaskModel.id == task_id.value).first()
        if task_model:
            self.db.delete(task_model)
            self.db.commit()

    async def list_by_assignee(self, assignee_id: UserId, project_id: Optional[str] = None) -> List[Task]:
        """Получить список задач по исполнителю."""
        query = self.db.query(TaskModel).filter(TaskModel.assignee_id == assignee_id.value)
        if project_id:
            query = query.filter(TaskModel.project_id == project_id)
        task_models = query.all()
        return [self._to_domain(model) for model in task_models]

    async def list_by_creator(self, creator_id: UserId, project_id: Optional[str] = None) -> List[Task]:
        """Получить список задач по создателю."""
        query = self.db.query(TaskModel).filter(TaskModel.creator_id == creator_id.value)
        if project_id:
            query = query.filter(TaskModel.project_id == project_id)
        task_models = query.all()
        return [self._to_domain(model) for model in task_models]

    async def list_by_project(self, project_id: str) -> List[Task]:
        """Получить список всех задач проекта."""
        task_models = self.db.query(TaskModel).filter(TaskModel.project_id == project_id).all()
        return [self._to_domain(model) for model in task_models]

    async def list_overdue(self, project_id: Optional[str] = None) -> List[Task]:
        """Получить список просроченных задач."""
        now = datetime.utcnow()
        query = self.db.query(TaskModel).filter(
            TaskModel.deadline < now,
            TaskModel.status != TaskStatus.COMPLETED.value
        )
        if project_id:
            query = query.filter(TaskModel.project_id == project_id)
        task_models = query.all()
        return [self._to_domain(model) for model in task_models]

    async def list_by_date_range(
        self, start_date: datetime, end_date: datetime, project_id: Optional[str] = None
    ) -> List[Task]:
        """Получить список задач в диапазоне дат."""
        query = self.db.query(TaskModel).filter(
            TaskModel.created_at >= start_date,
            TaskModel.created_at <= end_date
        )
        if project_id:
            query = query.filter(TaskModel.project_id == project_id)
        task_models = query.all()
        return [self._to_domain(model) for model in task_models]

    def _to_domain(self, model: TaskModel) -> Task:
        """Преобразовать модель БД в доменную сущность."""
        if not model:
            return None

        from ...domain.value_objects import CategoryId, Deadline, Comment, PhotoUrl

        return Task(
            id=TaskId(value=model.id),
            title=model.title,
            description=model.description,
            status=TaskStatus(model.status),
            priority=TaskPriority(model.priority),
            category_id=CategoryId(value=model.category_id) if model.category_id else None,
            assignee_id=UserId(value=model.assignee_id) if model.assignee_id else None,
            creator_id=UserId(value=model.creator_id),
            deadline=Deadline(value=model.deadline) if model.deadline else None,
            created_at=model.created_at,
            updated_at=model.updated_at,
            completed_at=model.completed_at,
            completion_photos=[PhotoUrl(value=photo) for photo in model.completion_photos] if model.completion_photos else [],
            completion_comment=Comment(value=model.completion_comment) if model.completion_comment else None,
            project_id=model.project_id,
        )

