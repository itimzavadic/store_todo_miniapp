# Store Todo Miniapp

Приложение для управления задачами, командой и складом через Telegram Mini App.

## Быстрый старт

### 1. Установка зависимостей

```bash
cd backend
pip install -r requirements.txt
```

### 2. Настройка окружения

Создайте файл `.env` в корне проекта:

```env
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
ENV=development
```

### 3. Запуск приложения

```bash
cd backend
uvicorn app.main:app --reload --port 8001
```

Приложение будет доступно по адресу: http://localhost:8001

### 4. Настройка Telegram Mini App

См. подробную инструкцию в [TELEGRAM_SETUP.md](TELEGRAM_SETUP.md)

### 3. Проверка работы

Откройте в браузере:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

### 4. Тестирование API

Запустите тестовый скрипт:

```bash
cd backend
python test_api.py
```

## Архитектура

Проект построен на принципах **Clean Architecture**:

- **Domain Layer** - доменные сущности и бизнес-логика
- **Application Layer** - use cases и интерфейсы репозиториев
- **Infrastructure Layer** - реализация репозиториев и БД
- **Presentation Layer** - API endpoints и схемы

Подробнее см. [ARCHITECTURE.md](ARCHITECTURE.md)

## Что реализовано

✅ Доменные сущности (User, Task, Product, Category)  
✅ Value Objects и Enums  
✅ Интерфейсы репозиториев  
✅ Use Cases для задач и пользователей  
✅ База данных (SQLite + SQLAlchemy)  
✅ Реализации репозиториев  
✅ API endpoints для задач и пользователей  
✅ Pydantic схемы для валидации  
✅ Авторизация через Telegram  
✅ Telegram Mini App интерфейс  
✅ Интеграция с Telegram Web App API  

## Что в разработке

⏳ Репозитории для Product и Category  
⏳ API endpoints для товаров и категорий  
⏳ Загрузка файлов (фото)  
⏳ Расширенная аналитика  

## API Endpoints

### Health
- `GET /api/v1/health` - Проверка работоспособности

### Tasks
- `POST /api/v1/tasks` - Создать задачу
- `GET /api/v1/tasks` - Получить список задач
- `GET /api/v1/tasks/{id}` - Получить задачу по ID
- `POST /api/v1/tasks/{id}/complete` - Выполнить задачу

### Users
- `POST /api/v1/users` - Создать пользователя
- `GET /api/v1/users` - Получить список пользователей
- `GET /api/v1/users/{id}` - Получить пользователя по ID
- `GET /api/v1/users/telegram/{telegram_id}` - Получить пользователя по Telegram ID

## Пример использования

### Создание пользователя

```bash
curl -X POST "http://localhost:8000/api/v1/users" \
  -H "Content-Type: application/json" \
  -d '{
    "telegram_id": 123456789,
    "username": "test_user",
    "full_name": "Тестовый Пользователь",
    "role": "owner"
  }'
```

### Создание задачи

```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Тестовая задача",
    "description": "Описание задачи",
    "priority": "high",
    "assignee_id": "user_id"
  }'
```

### Выполнение задачи

```bash
curl -X POST "http://localhost:8000/api/v1/tasks/{task_id}/complete" \
  -H "Content-Type: application/json" \
  -d '{
    "comment": "Задача выполнена!",
    "photos": ["https://example.com/photo.jpg"]
  }'
```

## Разработка

### Структура проекта

```
backend/app/
├── domain/          # Доменный слой
├── application/     # Прикладной слой
├── infrastructure/  # Инфраструктурный слой
├── presentation/    # Слой представления
└── main.py         # Точка входа
```

### Тестирование

```bash
# Запуск тестов
cd backend
pytest tests/

# Запуск тестового скрипта
python test_api.py
```

## Документация

- [QUICK_START.md](QUICK_START.md) - Быстрый старт
- [TELEGRAM_SETUP.md](TELEGRAM_SETUP.md) - Настройка Telegram Mini App
- [ARCHITECTURE.md](ARCHITECTURE.md) - Архитектура проекта

## Лицензия

MIT

