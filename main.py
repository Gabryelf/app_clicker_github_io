import flet as ft
import httpx
import json
import uuid 

GIST_ID = 'your_gist_id'
GITHUB_TOKEN = 'your_github_token'
GIST_URL = f'https://api.github.com/gists/{GIST_ID}'

async def read_data():
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(GIST_URL, headers=headers)
        if response.status_code == 200:
            gist_content = response.json()
            file_content = next(iter(gist_content['files'].values()))['content']
            try:
                return json.loads(file_content)
            except json.JSONDecodeError:
                print("Failed to decode JSON:", file_content)
                return {}
        else:
            print(f"Failed to fetch data: {response.status_code} {response.text}")
            return {}

async def write_data(data):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }
    data_str = json.dumps(data, indent=2)
    files = {
        "data.txt": {
            "content": data_str
        }
    }
    payload = {
        "files": files
    }
    async with httpx.AsyncClient() as client:
        response = await client.patch(GIST_URL, headers=headers, json=payload)
        return response.status_code == 200

async def main(page: ft.Page):
    page.title = "Flet App with Gist DB"

    user_id = str(uuid.uuid4())  # Используем uuid для генерации уникального идентификатора
    user_data = await read_data()

    name_input = ft.TextField(label="Enter your name", autofocus=True)
    
    async def enter_click(event):
        name = name_input.value
        user_data[user_id] = {"name": name}
        success = await write_data(user_data)
        if success:
            update_ui(name)
        else:
            page.add(ft.Text("Error writing data!"))
            page.update()

    def update_ui(name=""):
        page.controls.clear()
        if name:
            greeting = ft.Text(f"Welcome back, {name}!")
            page.add(greeting)
        else:
            enter_button = ft.TextButton(text="Enter", on_click=enter_click)
            page.add(name_input, enter_button)
        page.update()

    name = user_data.get(user_id, {}).get("name")
    update_ui(name)

if __name__ == "__main__":
    ft.app(target=main)
