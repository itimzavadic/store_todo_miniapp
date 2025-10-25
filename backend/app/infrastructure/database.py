"""Конфигурация базы данных."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..config.settings import get_settings

settings = get_settings()

# SQLite для начала, потом можно заменить на PostgreSQL
DATABASE_URL = "sqlite:///./store_todo.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Получить сессию базы данных."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

