# Инструкция по настройке Telegram Mini App

## Шаг 1: Создание Telegram бота

1. Откройте Telegram и найдите @BotFather
2. Отправьте команду `/newbot`
3. Введите имя бота (например: `Store Todo Bot`)
4. Введите username бота (например: `store_todo_bot`)
5. Сохраните токен бота (выглядит как `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

## Шаг 2: Настройка Mini App

1. Отправьте @BotFather команду `/newapp`
2. Выберите вашего бота из списка
3. Введите название приложения (например: `Store Todo`)
4. Введите описание (например: `Управление задачами для магазина`)
5. Загрузите иконку (опционально)
6. Введите URL вашего приложения (например: `https://your-domain.com/`)
7. Сохраните App ID

## Шаг 3: Настройка Backend

### Для локальной разработки:

1. Установите ngrok для создания туннеля:
   ```bash
   # Скачайте ngrok с https://ngrok.com/
   # Или через npm: npm install -g ngrok
   ```

2. Запустите ngrok:
   ```bash
   ngrok http 8001
   ```

3. Скопируйте HTTPS URL (например: `https://abc123.ngrok.io`)

### Для продакшена:

1. Разместите приложение на сервере (Heroku, Railway, DigitalOcean и т.д.)
2. Получите публичный URL вашего приложения

## Шаг 4: Обновление настроек

1. Откройте файл `backend/app/config/settings.py`
2. Добавьте токен бота:
   ```python
   class Settings(BaseSettings):
       app_version: str = "0.1.0"
       env: str = "development"
       telegram_bot_token: str = "YOUR_BOT_TOKEN_HERE"
       
       class Config:
           env_file = ".env"
           env_file_encoding = "utf-8"
   ```

3. Создайте файл `.env` в корне проекта:
   ```
   TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
   ENV=development
   ```

## Шаг 5: Обновление фронтенда

1. Откройте файл `frontend/index.html`
2. Найдите строку:
   ```javascript
   const API_URL = 'http://localhost:8001/api/v1';
   ```
3. Замените на ваш публичный URL:
   ```javascript
   const API_URL = 'https://your-domain.com/api/v1';
   ```

## Шаг 6: Тестирование

1. Запустите сервер:
   ```bash
   cd backend
   uvicorn app.main:app --reload --port 8001
   ```

2. Откройте Telegram и найдите вашего бота
3. Отправьте команду `/start`
4. Нажмите на кнопку Mini App (если настроена)
5. Проверьте работу интерфейса

## Шаг 7: Добавление кнопки Mini App

1. Отправьте @BotFather команду `/setmenubutton`
2. Выберите вашего бота
3. Введите текст кнопки (например: `Открыть приложение`)
4. Введите URL вашего приложения

## Полезные команды

- `/start` - Начать работу с ботом
- `/help` - Получить помощь
- `/settings` - Настройки бота

## Отладка

Если Mini App не работает:

1. Проверьте URL в настройках бота
2. Проверьте что сервер запущен
3. Проверьте логи сервера
4. Проверьте консоль браузера (F12)

## Безопасность

- Не публикуйте токен бота в открытом доступе
- Используйте HTTPS для продакшена
- Проверяйте подпись initData на сервере

