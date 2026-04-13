# Todo List API

REST API для управления списком задач (Todo list) на FastAPI с хранением данных в SQLite БД.

## Функциональность

- Получение списка всех задач с пагинацией и фильтрацией
- Получение задачи по ID
- Создание новой задачи
- Обновление существующей задачи
- Удаление задачи

## Технологии

- FastAPI
- Pydantic
- Uvicorn
- SQLite для хранения данных

## Запуск

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

2. Запустите сервер:
   ```bash
   python main.py
   ```

   Или с автоперезагрузкой:
   ```bash
   uvicorn main:app --reload
   ```

Сервер будет доступен по адресу `http://0.0.0.0:8000`.

## Документация API

Документация доступна по адресу `http://0.0.0.0:8000/docs` (Swagger UI).

## Эндпоинты

- `GET /tasks` - Получить все задачи с пагинацией и фильтрацией
  - Параметры: `skip` (int), `limit` (int), `done` (bool, опционально)
- `GET /tasks/{id}` - Получить задачу по ID
- `POST /tasks` - Создать новую задачу
- `PUT /tasks/{id}` - Обновить задачу
- `DELETE /tasks/{id}` - Удалить задачу

## Формат данных

Задача имеет следующие поля:
- `id` (int): Уникальный идентификатор
- `title` (str): Название задачи
- `done` (bool): Статус выполнения

## Хранение данных

Данные хранятся в БД SQLite `tasks.db` с таблицей `tasks`:
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done BOOLEAN DEFAULT FALSE
)
```

## Примеры запросов

### Получить все задачи
```bash
curl http://localhost:8000/tasks
```

### Получить невыполненные задачи
```bash
curl "http://localhost:8000/tasks?done=false"
```

### Создать новую задачу
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Купить молоко", "done": false}'
```

### Обновить задачу
```bash
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'
```

### Удалить задачу
```bash
curl -X DELETE http://localhost:8000/tasks/1
```