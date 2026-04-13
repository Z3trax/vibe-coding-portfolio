from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
import os

# Создаем приложение FastAPI
app = FastAPI(title="Todo List API", description="API для управления списком задач")

# Путь к БД
DATABASE = "tasks.db"

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

# Функция для инициализации БД
def init_db():
    """Инициализирует БД SQLite с таблицей tasks"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Создаем таблицу, если её нет
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done BOOLEAN DEFAULT FALSE
            )
        """)
        
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Ошибка при инициализации БД: {e}")

# Функция для получения одной задачи по ID
def get_task_from_db(task_id: int) -> Optional[dict]:
    """Получает задачу из БД по ID"""
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return dict(row)
        return None
    except sqlite3.Error as e:
        print(f"Ошибка при чтении из БД: {e}")
        return None

# Функция для получения всех задач с пагинацией и фильтрацией
def get_all_tasks_from_db(skip: int = 0, limit: int = 10, done: Optional[bool] = None) -> List[dict]:
    """Получает все задачи из БД с пагинацией и фильтрацией"""
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Строим SQL запрос с фильтрацией
        if done is not None:
            cursor.execute("SELECT id, title, done FROM tasks WHERE done = ? ORDER BY id LIMIT ? OFFSET ?", 
                         (done, limit, skip))
        else:
            cursor.execute("SELECT id, title, done FROM tasks ORDER BY id LIMIT ? OFFSET ?", 
                         (limit, skip))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        print(f"Ошибка при чтении из БД: {e}")
        return []

# Функция для добавления новой задачи
def add_task_to_db(title: str, done: bool = False) -> Optional[dict]:
    """Добавляет новую задачу в БД"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (title, done))
        conn.commit()
        
        task_id = cursor.lastrowid
        conn.close()
        
        # Возвращаем созданную задачу
        return get_task_from_db(task_id)
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении в БД: {e}")
        return None

# Функция для обновления задачи
def update_task_in_db(task_id: int, title: Optional[str] = None, done: Optional[bool] = None) -> Optional[dict]:
    """Обновляет задачу в БД"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Проверяем, существует ли задача
        cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
        if not cursor.fetchone():
            conn.close()
            return None
        
        # Строим запрос обновления
        if title is not None and done is not None:
            cursor.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?", 
                         (title, done, task_id))
        elif title is not None:
            cursor.execute("UPDATE tasks SET title = ? WHERE id = ?", (title, task_id))
        elif done is not None:
            cursor.execute("UPDATE tasks SET done = ? WHERE id = ?", (done, task_id))
        
        conn.commit()
        conn.close()
        
        return get_task_from_db(task_id)
    except sqlite3.Error as e:
        print(f"Ошибка при обновлении в БД: {e}")
        return None

# Функция для удаления задачи
def delete_task_from_db(task_id: int) -> bool:
    """Удаляет задачу из БД"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Проверяем, существует ли задача
        cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
        if not cursor.fetchone():
            conn.close()
            return False
        
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        
        return True
    except sqlite3.Error as e:
        print(f"Ошибка при удалении из БД: {e}")
        return False

# Инициализируем БД при запуске
init_db()

# Получить все задачи с пагинацией и фильтрацией
@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), done: Optional[bool] = None):
    """
    Получить все задачи с поддержкой пагинации и фильтрации по статусу.
    
    - skip: количество задач для пропуска (по умолчанию 0)
    - limit: количество задач для возврата (по умолчанию 10, максимум 100)
    - done: фильтр по статусу выполнения (опционально)
    """
    tasks = get_all_tasks_from_db(skip=skip, limit=limit, done=done)
    return [TaskResponse(**task) for task in tasks]

# Получить задачу по ID
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    """Получить одну задачу по ID"""
    task = get_task_from_db(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return TaskResponse(**task)

# Создать новую задачу
@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate):
    """Создать новую задачу"""
    new_task = add_task_to_db(task.title, task.done)
    if not new_task:
        raise HTTPException(status_code=500, detail="Ошибка при создании задачи")
    return TaskResponse(**new_task)

# Обновить задачу по ID
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate):
    """Обновить существующую задачу"""
    updated_task = update_task_in_db(task_id, task_update.title, task_update.done)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return TaskResponse(**updated_task)

# Удалить задачу по ID
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Удалить задачу по ID"""
    if not delete_task_from_db(task_id):
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return {"message": "Задача удалена"}

# Условие запуска сервера
if __name__ == "__main__":
    import uvicorn
    # Запуск без перезагрузки через python main.py
    # Для автоперезагрузки используйте: uvicorn main:app --reload
    uvicorn.run(app, host="0.0.0.0", port=8000)