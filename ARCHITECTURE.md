# Архитектура проекта Store Todo Miniapp

## Общая схема архитектуры

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                           │
│  (FastAPI Routes, Pydantic Schemas, API Endpoints)             │
├─────────────────────────────────────────────────────────────────┤
│  • /api/v1/health                                               │
│  • /api/v1/tasks (GET, POST, POST /complete)                   │
│  • /api/v1/users (GET, POST)                                   │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                            │
│  (Use Cases, Repository Interfaces)                             │
├─────────────────────────────────────────────────────────────────┤
│  Use Cases:                                                      │
│  • CreateTaskUseCase                                            │
│  • GetTaskUseCase                                               │
│  • CompleteTaskUseCase                                          │
│  • ListTasksUseCase                                             │
│  • CreateUserUseCase                                            │
│  • GetUserUseCase                                               │
│  • ListUsersUseCase                                             │
│                                                                 │
│  Repository Interfaces:                                         │
│  • UserRepository                                               │
│  • TaskRepository                                               │
│  • ProductRepository                                            │
│  • CategoryRepository                                           │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DOMAIN LAYER                               │
│  (Entities, Value Objects, Enums)                              │
├─────────────────────────────────────────────────────────────────┤
│  Entities:                                                       │
│  • User (с правами доступа)                                     │
│  • Task (с бизнес-логикой выполнения)                          │
│  • Product (управление складом)                                │
│  • Category                                                      │
│  • TaskTemplate                                                 │
│  • ProductSet                                                   │
│                                                                 │
│  Value Objects:                                                 │
│  • TaskId, UserId, ProductId, CategoryId                       │
│  • PhotoUrl, Barcode, Quantity, Deadline, Comment               │
│                                                                 │
│  Enums:                                                         │
│  • TaskStatus, TaskPriority                                     │
│  • UserRole, ProductStatus                                     │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                  INFRASTRUCTURE LAYER                           │
│  (Database, Repository Implementations)                         │
├─────────────────────────────────────────────────────────────────┤
│  Database:                                                      │
│  • SQLite (SQLAlchemy)                                          │
│  • Models: UserModel, TaskModel, ProductModel, CategoryModel   │
│                                                                 │
│  Repository Implementations:                                    │
│  • UserRepositoryImpl                                           │
│  • TaskRepositoryImpl                                           │
└─────────────────────────────────────────────────────────────────┘
```

## Структура директорий

```
backend/app/
├── domain/                    # Доменный слой
│   ├── enums.py              # Перечисления (TaskStatus, UserRole и т.д.)
│   ├── value_objects.py      # Value Objects (TaskId, UserId и т.д.)
│   ├── user.py               # Сущность User
│   ├── task.py               # Сущность Task
│   ├── product.py            # Сущность Product
│   ├── category.py          # Сущность Category
│   └── task_template.py      # TaskTemplate и ProductSet
│
├── application/              # Прикладной слой
│   ├── repositories/         # Интерфейсы репозиториев (порты)
│   │   ├── user_repository.py
│   │   ├── task_repository.py
│   │   ├── product_repository.py
│   │   └── category_repository.py
│   └── use_cases/            # Use cases
│       ├── task_use_cases.py
│       └── user_use_cases.py
│
├── infrastructure/            # Инфраструктурный слой
│   ├── database.py           # Конфигурация БД
│   ├── models.py             # SQLAlchemy модели
│   └── repositories/         # Реализации репозиториев
│       ├── user_repository_impl.py
│       └── task_repository_impl.py
│
├── presentation/             # Слой представления
│   ├── api.py                # Подключение роутов
│   ├── schemas/              # Pydantic схемы
│   │   ├── task_schemas.py
│   │   └── user_schemas.py
│   └── routes/               # API endpoints
│       ├── health.py
│       ├── tasks.py
│       └── users.py
│
└── main.py                   # Точка входа приложения
```

## Поток данных

### Создание задачи:

```
1. Client → POST /api/v1/tasks
2. Presentation Layer (routes/tasks.py)
   ↓
3. Application Layer (CreateTaskUseCase)
   ↓
4. Domain Layer (Task entity)
   ↓
5. Infrastructure Layer (TaskRepositoryImpl)
   ↓
6. Database (SQLite)
```

### Выполнение задачи:

```
1. Client → POST /api/v1/tasks/{id}/complete
2. Presentation Layer (routes/tasks.py)
   ↓
3. Application Layer (CompleteTaskUseCase)
   ↓
4. Domain Layer (Task.mark_as_completed())
   ↓
5. Infrastructure Layer (TaskRepositoryImpl.update())
   ↓
6. Database (SQLite)
```

## Принципы Clean Architecture

1. **Зависимости направлены внутрь**: Внешние слои зависят от внутренних
2. **Интерфейсы на границах**: Репозитории объявлены в application, реализованы в infrastructure
3. **Бизнес-логика в domain**: Вся логика в доменных сущностях
4. **Тестируемость**: Каждый слой можно тестировать независимо

## API Endpoints

### Health Check
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

## База данных

### Таблицы:
- `users` - Пользователи
- `tasks` - Задачи
- `products` - Товары
- `categories` - Категории

### Связи:
- Task → User (creator_id, assignee_id)
- Task → Category (category_id)
- Product → Category (category_id)

