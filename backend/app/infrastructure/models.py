"""SQLAlchemy модели для базы данных."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import JSON

from .database import Base
from ..domain.enums import TaskStatus, TaskPriority, UserRole, ProductStatus


class UserModel(Base):
    """Модель пользователя в БД."""

    __tablename__ = "users"

    id = Column(String, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    project_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CategoryModel(Base):
    """Модель категории в БД."""

    __tablename__ = "categories"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    color = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    project_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TaskModel(Base):
    """Модель задачи в БД."""

    __tablename__ = "tasks"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(SQLEnum(TaskStatus), nullable=False)
    priority = Column(SQLEnum(TaskPriority), nullable=False)
    category_id = Column(String, ForeignKey("categories.id"), nullable=True)
    assignee_id = Column(String, ForeignKey("users.id"), nullable=True)
    creator_id = Column(String, ForeignKey("users.id"), nullable=False)
    deadline = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    completion_photos = Column(JSON, nullable=True)  # Список URL фотографий
    completion_comment = Column(Text, nullable=True)
    project_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ProductModel(Base):
    """Модель товара в БД."""

    __tablename__ = "products"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    quantity = Column(Integer, nullable=False, default=0)
    category_id = Column(String, ForeignKey("categories.id"), nullable=True)
    photo_url = Column(String, nullable=True)
    barcode = Column(String, nullable=True, unique=True)
    status = Column(SQLEnum(ProductStatus), nullable=False)
    project_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

