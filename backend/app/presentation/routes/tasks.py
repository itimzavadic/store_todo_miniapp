"""Роуты для работы с задачами."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from ...application.use_cases.task_use_cases import (
    CompleteTaskUseCase,
    CreateTaskUseCase,
    GetTaskUseCase,
    ListTasksUseCase,
)
from ...domain.enums import TaskPriority
from ...domain.value_objects import CategoryId, TaskId, UserId
from ...infrastructure.database import get_db
from ...infrastructure.repositories import TaskRepositoryImpl, UserRepositoryImpl
from ..middleware.telegram_auth import require_auth
from ..schemas import TaskComplete, TaskCreate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])


async def get_task_repository(db: Session = Depends(get_db)) -> TaskRepositoryImpl:
    """Получить репозиторий задач."""
    return TaskRepositoryImpl(db)


async def get_user_repository(db: Session = Depends(get_db)) -> UserRepositoryImpl:
    """Получить репозиторий пользователей."""
    return UserRepositoryImpl(db)


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: Request,
    task_data: TaskCreate,
    task_repo: TaskRepositoryImpl = Depends(get_task_repository),
    user_repo: UserRepositoryImpl = Depends(get_user_repository),
):
    """Создать новую задачу."""
    try:
        # Получаем Telegram ID из авторизации
        telegram_id = await require_auth(request)
        creator_id = UserId(value=str(telegram_id))

        use_case = CreateTaskUseCase(task_repo, user_repo)
        task = await use_case.execute(
            title=task_data.title,
            creator_id=creator_id,
            description=task_data.description,
            priority=task_data.priority,
            category_id=CategoryId(value=task_data.category_id) if task_data.category_id else None,
            assignee_id=UserId(value=task_data.assignee_id) if task_data.assignee_id else None,
            deadline=None,  # TODO: Добавить поддержку deadline
        )
        return _task_to_response(task)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str, task_repo: TaskRepositoryImpl = Depends(get_task_repository)):
    """Получить задачу по ID."""
    use_case = GetTaskUseCase(task_repo)
    task = await use_case.execute(TaskId(value=task_id))
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")
    return _task_to_response(task)


@router.post("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(
    task_id: str,
    complete_data: TaskComplete,
    task_repo: TaskRepositoryImpl = Depends(get_task_repository),
):
    """Отметить задачу как выполненную."""
    try:
        use_case = CompleteTaskUseCase(task_repo)
        task = await use_case.execute(
            TaskId(value=task_id),
            comment=complete_data.comment,
            photos=complete_data.photos,
        )
        return _task_to_response(task)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[TaskResponse])
async def list_tasks(
    assignee_id: Optional[str] = None,
    creator_id: Optional[str] = None,
    project_id: Optional[str] = None,
    task_repo: TaskRepositoryImpl = Depends(get_task_repository),
):
    """Получить список задач."""
    use_case = ListTasksUseCase(task_repo)
    tasks = await use_case.execute(
        assignee_id=UserId(value=assignee_id) if assignee_id else None,
        creator_id=UserId(value=creator_id) if creator_id else None,
        project_id=project_id,
    )
    return [_task_to_response(task) for task in tasks]


def _task_to_response(task) -> TaskResponse:
    """Преобразовать доменную задачу в схему ответа."""
    return TaskResponse(
        id=task.id.value,
        title=task.title,
        description=task.description,
        priority=task.priority,
        category_id=task.category_id.value if task.category_id else None,
        assignee_id=task.assignee_id.value if task.assignee_id else None,
        deadline=None,  # TODO: Добавить поддержку deadline
        status=task.status,
        creator_id=task.creator_id.value,
        created_at=task.created_at,
        updated_at=task.updated_at,
        completed_at=task.completed_at,
        completion_photos=[photo.value for photo in task.completion_photos] if task.completion_photos else None,
        completion_comment=task.completion_comment.value if task.completion_comment else None,
        project_id=task.project_id,
    )

