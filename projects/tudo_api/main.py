from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import json
import os

# Создаем приложение FastAPI
app = FastAPI(title="Todo List API", description="API для управления списком задач")

# Путь к файлу с данными
TASKS_FILE = "tasks.json"

# Модели Pydantic
class TaskCreate(BaseModel):
    title: str
    done: bool = False

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    done: bool

# Функция для загрузки задач из файла
def load_tasks() -> List[dict]:
    if not os.path.exists(TASKS_FILE):
        # Если файл не существует, создаем пустой список
        with open(TASKS_FILE, 'w') as f:
            json.dump([], f)
        return []
    with open(TASKS_FILE, 'r') as f:
        return json.load(f)

# Функция для сохранения задач в файл
def save_tasks(tasks: List[dict]):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

# Получить все задачи
@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks():
    tasks = load_tasks()
    return [TaskResponse(**task) for task in tasks]

# Получить задачу по ID
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            return TaskResponse(**task)
    raise HTTPException(status_code=404, detail="Задача не найдена")

# Создать новую задачу
@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate):
    tasks = load_tasks()
    # Находим максимальный ID и увеличиваем на 1
    max_id = max([t["id"] for t in tasks], default=0)
    new_task = {"id": max_id + 1, "title": task.title, "done": task.done}
    tasks.append(new_task)
    save_tasks(tasks)
    return TaskResponse(**new_task)

# Обновить задачу по ID
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate):
    tasks = load_tasks()
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            if task_update.title is not None:
                task["title"] = task_update.title
            if task_update.done is not None:
                task["done"] = task_update.done
            save_tasks(tasks)
            return TaskResponse(**task)
    raise HTTPException(status_code=404, detail="Задача не найдена")

# Удалить задачу по ID
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = load_tasks()
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            save_tasks(tasks)
            return {"message": "Задача удалена"}
    raise HTTPException(status_code=404, detail="Задача не найдена")

# Условие запуска сервера
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)