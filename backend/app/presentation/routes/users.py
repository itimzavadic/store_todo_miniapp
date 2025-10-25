"""Роуты для работы с пользователями."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from ...application.use_cases.user_use_cases import CreateUserUseCase, GetUserUseCase, ListUsersUseCase
from ...domain.enums import UserRole
from ...domain.value_objects import UserId
from ...infrastructure.database import get_db
from ...infrastructure.repositories import UserRepositoryImpl
from ..middleware.telegram_auth import get_current_user, require_auth
from ..schemas import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


async def get_user_repository(db: Session = Depends(get_db)) -> UserRepositoryImpl:
    """Получить репозиторий пользователей."""
    return UserRepositoryImpl(db)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: Request,
    user_data: UserCreate,
    user_repo: UserRepositoryImpl = Depends(get_user_repository),
):
    """Создать нового пользователя."""
    try:
        # Получаем Telegram ID из авторизации
        telegram_id = await require_auth(request)
        
        # Используем данные из запроса или из авторизации
        use_case = CreateUserUseCase(user_repo)
        user = await use_case.execute(
            telegram_id=telegram_id,
            username=user_data.username,
            full_name=user_data.full_name,
            role=user_data.role,
            project_id=user_data.project_id,
        )
        return _user_to_response(user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, user_repo: UserRepositoryImpl = Depends(get_user_repository)):
    """Получить пользователя по ID."""
    use_case = GetUserUseCase(user_repo)
    user = await use_case.execute(UserId(value=user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return _user_to_response(user)


@router.get("/", response_model=List[UserResponse])
async def list_users(
    project_id: Optional[str] = None,
    active_only: bool = False,
    user_repo: UserRepositoryImpl = Depends(get_user_repository),
):
    """Получить список пользователей."""
    use_case = ListUsersUseCase(user_repo)
    users = await use_case.execute(project_id=project_id, active_only=active_only)
    return [_user_to_response(user) for user in users]


@router.get("/telegram/{telegram_id}", response_model=UserResponse)
async def get_user_by_telegram_id(
    telegram_id: int, user_repo: UserRepositoryImpl = Depends(get_user_repository)
):
    """Получить пользователя по Telegram ID."""
    use_case = GetUserUseCase(user_repo)
    user = await use_case.execute_by_telegram_id(telegram_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return _user_to_response(user)


def _user_to_response(user) -> UserResponse:
    """Преобразовать доменного пользователя в схему ответа."""
    return UserResponse(
        id=user.id.value,
        telegram_id=user.telegram_id,
        username=user.username,
        full_name=user.full_name,
        role=user.role,
        is_active=user.is_active,
        project_id=user.project_id,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )

