import flet as ft
import asyncio
from pymongo import MongoClient
from bson.objectid import ObjectId



# Установите соединение с базой данных
client = MongoClient('mongodb+srv://eleronsmarya:l2kKlf3xMrWVadQ9@cluster1.lgx1gsg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1')
db = client['data_app']


def get_or_create_user(session_id):
    user_data = db.users.find_one({'session_id': session_id})
    if not user_data:
        # Создаем нового пользователя с уникальным ID сессии
        user_data = {
            'session_id': session_id,
            'name': None
        }
        db.users.insert_one(user_data)
    return user_data

def save_user_name(session_id, name):
    db.users.update_one({'session_id': session_id}, {'$set': {'name': name}})

async def main(page: ft.Page):
    page.title = "MongoDB Flet App"

    # Инициализация переменной сессии
    session_id = str(ObjectId())

    user_data = get_or_create_user(session_id)

    if user_data['name']:
        # Если имя пользователя уже сохранено, показываем приветствие
        greeting = ft.Text(f"Welcome back, {user_data['name']}!")
        page.add(greeting)
    else:
        # Если имя пользователя не сохранено, запрашиваем его
        name_input = ft.TextField(label="Enter your name", autofocus=True)
        enter_button = ft.TextButton(text="Enter", on_click=lambda e: enter_click(e, name_input, session_id, page))
        page.add(name_input, enter_button)

    await page.update()

async def enter_click(event, name_input, session_id, page):
    # Сохраняем имя пользователя в базе данных
    save_user_name(session_id, name_input.value)
    # Обновляем страницу, показываем приветствие
    page.controls.clear()
    greeting = ft.Text(f"Welcome, {name_input.value}!")
    page.add(greeting)
    await page.update()

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)
