# Быстрый старт

## 1. Установка зависимостей

```bash
cd backend
pip install -r requirements.txt
```

## 2. Настройка окружения

Создайте файл `.env` в корне проекта:

```env
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
ENV=development
```

## 3. Запуск сервера

```bash
cd backend
uvicorn app.main:app --reload --port 8001
```

## 4. Доступ к приложению

- **Локально**: http://localhost:8001/
- **API Docs**: http://localhost:8001/docs
- **Health Check**: http://localhost:8001/api/v1/health

## 5. Тестирование в Telegram

1. Создайте бота через @BotFather
2. Настройте Mini App (см. TELEGRAM_SETUP.md)
3. Откройте бота в Telegram
4. Нажмите на кнопку Mini App

## 6. Структура проекта

```
store_todo_miniapp/
├── backend/          # Backend (FastAPI)
│   ├── app/
│   │   ├── domain/   # Доменный слой
│   │   ├── application/  # Use cases
│   │   ├── infrastructure/  # БД, репозитории
│   │   └── presentation/  # API, роуты
│   └── requirements.txt
├── frontend/        # Frontend (HTML/CSS/JS)
│   └── index.html
└── PROJECT          # Описание проекта
```

## 7. API Endpoints

- `GET /api/v1/health` - Health check
- `GET /api/v1/tasks` - Список задач
- `POST /api/v1/tasks` - Создать задачу
- `POST /api/v1/tasks/{id}/complete` - Выполнить задачу
- `GET /api/v1/users` - Список пользователей
- `POST /api/v1/users` - Создать пользователя

## 8. Следующие шаги

1. Настройте Telegram бота (см. TELEGRAM_SETUP.md)
2. Протестируйте API через Swagger UI
3. Протестируйте интерфейс в Telegram
4. Добавьте недостающий функционал

## 9. Разработка

Для разработки используйте:

```bash
# Запуск сервера с автоперезагрузкой
uvicorn app.main:app --reload --port 8001

# Запуск тестов
python test_api.py
```

## 10. Проблемы?

См. TELEGRAM_SETUP.md для инструкций по настройке Telegram Mini App.

