# Task API

REST API для управления задачами. Демонстрирует современный стек асинхронного Python-бэкенда: FastAPI, SQLAlchemy 2.0 (async), PostgreSQL, Alembic, Docker.

## Стек

- **Python** 3.13
- **FastAPI** — веб-фреймворк
- **SQLAlchemy 2.0** (async) + **asyncpg** — работа с БД
- **Pydantic v2** + **pydantic-settings** — валидация и конфигурация
- **Alembic** — миграции
- **PostgreSQL 18**
- **pytest** + **httpx** + **aiosqlite** — тесты
- **uv** — управление зависимостями
- **Docker** + **docker-compose** — окружение

## Быстрый старт

### Через Docker (рекомендуется)

```bash
git clone <url-репозитория>
cd task-api

cp .env.example .env

docker compose up --build
```

Приложение будет доступно на http://localhost:8000.

Swagger UI: http://localhost:8000/docs

### Локально

Требуется Python 3.13+, PostgreSQL и [uv](https://docs.astral.sh/uv/).

```bash
# Установить зависимости
uv sync

# Создать .env
cp .env.example .env

# Запустить Postgres
docker compose up -d db

# Применить миграции
uv run alembic upgrade head

# Запустить сервер
uv run uvicorn app.main:app --reload
```

## Примеры использования

### Создать задачу

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn FastAPI", "description": "Read docs"}'
```

Ответ:

```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "description": "Read docs",
  "status": "todo",
  "created_at": "2026-10-14T12:00:00Z"
}
```

### Получить список задач

```bash
curl http://localhost:8000/tasks
```

### Получить задачу по id

```bash
curl http://localhost:8000/tasks/1
```

### Обновить задачу

```bash
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn FastAPI", "description": "Read docs", "status": "done"}'
```

### Удалить задачу

```bash
curl -X DELETE http://localhost:8000/tasks/1
```

## Эндпоинты

| Метод  | Путь          | Описание          | Коды ответа  |
|--------|---------------|-------------------|--------------|
| GET    | `/health`     | Проверка живости  | 200          |
| POST   | `/tasks`      | Создать задачу    | 201, 422     |
| GET    | `/tasks`      | Список задач      | 200          |
| GET    | `/tasks/{id}` | Получить задачу   | 200, 404     |
| PUT    | `/tasks/{id}` | Обновить задачу   | 200, 404, 422|
| DELETE | `/tasks/{id}` | Удалить задачу    | 204, 404     |

Полная документация — в Swagger UI: `/docs`.

## Статусы задач

- `todo` — новая задача
- `in_progress` — в работе
- `done` — завершена

## Структура проекта

```
task-api/
├── app/
│   ├── __init__.py
│   ├── main.py           # точка входа FastAPI
│   ├── config.py         # настройки через pydantic-settings
│   ├── database.py       # async engine, session, Base
│   ├── models.py         # ORM-модели
│   ├── schemas.py        # Pydantic-схемы
│   ├── crud.py           # функции работы с БД
│   └── routers/
│       ├── __init__.py
│       └── tasks.py      # HTTP-эндпоинты
├── alembic/
│   └── versions/         # файлы миграций
├── tests/
│   ├── conftest.py       # фикстуры pytest
│   └── test_tasks.py     # тесты эндпоинтов
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── pyproject.toml
├── uv.lock
├── .env.example
└── README.md
```

## Тесты

```bash
uv run pytest
```

Тесты используют SQLite в памяти через `aiosqlite`. Это быстро и не требует запущенного PostgreSQL. Покрытие — 14 тестов: CRUD, валидация, обработка ошибок (404, 422).

## Миграции

```bash
# Создать новую миграцию
uv run alembic revision --autogenerate -m "описание изменения"

# Применить
uv run alembic upgrade head

# Откатить последнюю
uv run alembic downgrade -1
```

## Конфигурация

Настройки читаются из переменных окружения с префиксом `APP_`:

| Переменная           | Описание                          | Пример                                            |
|----------------------|-----------------------------------|---------------------------------------------------|
| `APP_DATABASE_URL`   | URL подключения к PostgreSQL      | `postgresql+asyncpg://user:pass@localhost:5432/db`|
| `APP_DEBUG`          | Debug-режим (логи SQL, traceback) | `true` / `false`                                  |

Скопируй `.env.example` в `.env` и подставь свои значения. Файл `.env` в `.gitignore` — в репозиторий не попадает.

## Что реализовано

- CRUD по сущности `Task`
- Валидация входных данных через Pydantic
- Миграции через Alembic
- Асинхронная работа с БД (asyncpg)
- Docker-окружение (приложение + БД)
- Тесты через pytest (14 штук)
- Обработка ошибок (404, 422)
- Health-check

## Что не реализовано (сознательно)

- **Аутентификация** — API открыт, в проекте нет пользователей
- **Пагинация** — на малых данных избыточна
- **Кэширование (Redis)** — нагрузка на чтение низкая, кэш не дал бы выигрыша
- **Фоновые задачи (Celery / RabbitMQ)** — нет операций, которые нужно выносить в очереди
- **Rate limiting** — проект локальный, не публичный
- **Мониторинг (Prometheus, Sentry)** — не требуется для демонстрационного проекта