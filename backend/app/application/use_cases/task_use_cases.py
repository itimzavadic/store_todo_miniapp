"""Use cases для работы с задачами."""

from datetime import datetime
from typing import List, Optional

from ...domain.task import Task
from ...domain.enums import TaskPriority, TaskStatus
from ...domain.value_objects import CategoryId, Deadline, TaskId, UserId
from ..repositories import TaskRepository, UserRepository


class CreateTaskUseCase:
    """Use case для создания задачи."""

    def __init__(self, task_repository: TaskRepository, user_repository: UserRepository):
        self.task_repository = task_repository
        self.user_repository = user_repository

    async def execute(
        self,
        title: str,
        creator_id: UserId,
        description: Optional[str] = None,
        priority: TaskPriority = TaskPriority.MEDIUM,
        category_id: Optional[CategoryId] = None,
        assignee_id: Optional[UserId] = None,
        deadline: Optional[Deadline] = None,
        project_id: Optional[str] = None,
    ) -> Task:
        """Создать новую задачу."""
        # Проверка существования пользователя
        creator = await self.user_repository.get_by_id(creator_id)
        if not creator:
            raise ValueError("Пользователь-создатель не найден")

        if assignee_id:
            assignee = await self.user_repository.get_by_id(assignee_id)
            if not assignee:
                raise ValueError("Исполнитель не найден")

        # Создание задачи
        task = Task(
            id=TaskId(value=str(datetime.utcnow().timestamp())),
            title=title,
            description=description,
            status=TaskStatus.PENDING,
            priority=priority,
            category_id=category_id,
            assignee_id=assignee_id,
            creator_id=creator_id,
            deadline=deadline,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            project_id=project_id,
        )

        return await self.task_repository.create(task)


class GetTaskUseCase:
    """Use case для получения задачи."""

    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    async def execute(self, task_id: TaskId) -> Optional[Task]:
        """Получить задачу по ID."""
        return await self.task_repository.get_by_id(task_id)


class CompleteTaskUseCase:
    """Use case для выполнения задачи."""

    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    async def execute(
        self, task_id: TaskId, comment: Optional[str] = None, photos: Optional[List[str]] = None
    ) -> Task:
        """Отметить задачу как выполненную."""
        task = await self.task_repository.get_by_id(task_id)
        if not task:
            raise ValueError("Задача не найдена")

        task.mark_as_completed(comment=comment, photos=photos)
        return await self.task_repository.update(task)


class ListTasksUseCase:
    """Use case для получения списка задач."""

    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    async def execute(
        self,
        assignee_id: Optional[UserId] = None,
        creator_id: Optional[UserId] = None,
        project_id: Optional[str] = None,
    ) -> List[Task]:
        """Получить список задач."""
        if assignee_id:
            return await self.task_repository.list_by_assignee(assignee_id, project_id)
        elif creator_id:
            return await self.task_repository.list_by_creator(creator_id, project_id)
        elif project_id:
            return await self.task_repository.list_by_project(project_id)
        else:
            return []

