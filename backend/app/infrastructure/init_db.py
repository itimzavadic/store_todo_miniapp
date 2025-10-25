"""Инициализация базы данных."""

from .database import Base, engine


def init_db():
    """Создать все таблицы в базе данных."""
    Base.metadata.create_all(bind=engine)
    print("База данных инициализирована успешно")


if __name__ == "__main__":
    init_db()

