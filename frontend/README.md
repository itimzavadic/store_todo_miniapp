# Store Todo Mini App - Frontend

Минимальный интерфейс Telegram Mini App для управления задачами.

## Функционал

- 📋 Просмотр списка задач
- ➕ Создание новых задач
- ✅ Выполнение задач
- 👤 Информация о пользователе

## Запуск

1. Откройте `index.html` в браузере
2. Или разместите на веб-сервере
3. Для тестирования в Telegram используйте бота с настроенным Mini App

## Интеграция с Telegram

Для работы в Telegram Mini App нужно:

1. Создать бота через @BotFather
2. Настроить Mini App URL в боте
3. Добавить кнопку для открытия Mini App

## API

Интерфейс работает с API по адресу `http://localhost:8001/api/v1`

### Endpoints

- `GET /tasks` - Получить список задач
- `POST /tasks` - Создать задачу
- `POST /tasks/{id}/complete` - Выполнить задачу

## Авторизация

Авторизация происходит автоматически через Telegram Web App API.
Telegram передаёт `initData` в заголовке `X-Telegram-Init-Data`.

