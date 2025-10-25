"""Скрипт для тестирования API."""

import asyncio
import httpx
from datetime import datetime


BASE_URL = "http://localhost:8001/api/v1"


async def test_health():
    """Тест health check."""
    print("\n=== Тест Health Check ===")
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")


async def test_create_user():
    """Тест создания пользователя."""
    print("\n=== Тест создания пользователя ===")
    async with httpx.AsyncClient(follow_redirects=True) as client:
        user_data = {
            "telegram_id": 123456789,
            "username": "test_user",
            "full_name": "Тестовый Пользователь",
            "role": "owner",
            "project_id": "test_project"
        }
        response = await client.post(f"{BASE_URL}/users", json=user_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200 or response.status_code == 201:
            print(f"Response: {response.json()}")
            return response.json()["id"]
        else:
            print(f"Error: {response.text}")
            return None


async def test_create_task(user_id: str):
    """Тест создания задачи."""
    print("\n=== Тест создания задачи ===")
    async with httpx.AsyncClient(follow_redirects=True) as client:
        task_data = {
            "title": "Тестовая задача",
            "description": "Описание тестовой задачи",
            "priority": "high",
            "assignee_id": user_id
        }
        response = await client.post(f"{BASE_URL}/tasks", json=task_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200 or response.status_code == 201:
            print(f"Response: {response.json()}")
            return response.json()["id"]
        else:
            print(f"Error: {response.text}")
            return None


async def test_list_tasks():
    """Тест получения списка задач."""
    print("\n=== Тест получения списка задач ===")
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(f"{BASE_URL}/tasks")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.json()


async def test_complete_task(task_id: str):
    """Тест выполнения задачи."""
    print("\n=== Тест выполнения задачи ===")
    async with httpx.AsyncClient(follow_redirects=True) as client:
        complete_data = {
            "comment": "Задача выполнена успешно!",
            "photos": ["https://example.com/photo1.jpg"]
        }
        response = await client.post(f"{BASE_URL}/tasks/{task_id}/complete", json=complete_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")


async def test_list_users():
    """Тест получения списка пользователей."""
    print("\n=== Тест получения списка пользователей ===")
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(f"{BASE_URL}/users")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")


async def run_all_tests():
    """Запустить все тесты."""
    print("=" * 50)
    print("ЗАПУСК ТЕСТОВ API")
    print("=" * 50)
    
    # Проверка health
    await test_health()
    
    # Создание пользователя
    user_id = await test_create_user()
    
    # Создание задачи
    task_id = await test_create_task(user_id)
    
    # Получение списка задач
    await test_list_tasks()
    
    # Выполнение задачи
    await test_complete_task(task_id)
    
    # Получение списка пользователей
    await test_list_users()
    
    print("\n" + "=" * 50)
    print("ТЕСТЫ ЗАВЕРШЕНЫ")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(run_all_tests())

