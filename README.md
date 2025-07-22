# CharityOps — Благотворительный фонд для поддержки кошек

CharityOps — это благотворительный фонд, который собирает пожертвования на различные целевые проекты, направленные на поддержку кошек. Фонд помогает с медицинским обслуживанием кошек, обустройством кошачьих колоний и покупкой корма для животных, оставшихся без попечения.

![Главная страница проекта](readme_images/main_images.png)

## Описание проекта

Проект включает в себя систему для управления пожертвованиями и проектами. Пользователи могут создавать пожертвования, а суперюзеры — создавать и управлять проектами для сбора средств. Каждый проект может быть связан с конкретной целью, такой как лечение кошек или поддержка кошачьих колоний.

## 🚀 Функциональность

- Создание благотворительных проектов (только для суперюзеров)
- Получение списка всех проектов
- Обновление и удаление проектов (только для суперюзеров)
- Создание пожертвований пользователями
- Получение списка всех пожертвований (только для суперюзеров)
- Получение истории пожертвований текущего пользователя
- Автоматическое распределение средств между проектами

## Эндпоинты API

### GoogleSheets (Google)

- `POST /google/` — Формирование гугл таблицы для закрытых проектов с периодом сборов средств.

### Проекты (Charity Projects)

- `POST /projects/` — Создание нового проекта.
- `GET /projects/` — Получение списка всех проектов.
- `DELETE /projects/{project_id}` — Удаление проекта.
- `PATCH /projects/{project_id}` — Обновление проекта.

### Пожертвования (Donations)

- `POST /donations/` — Создание нового пожертвования.
- `GET /donations/` — Получение списка всех пожертвований (для суперюзеров).
- `GET /donations/my` — Получение списка пожертвований текущего пользователя.

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/ShiroyashaSG/CharityOps.git
   ```
2. Перейдите в директорию проекта:
   ```bash
   cd CharityOps
   ```
3. Cоздайте и активируйте виртуальное окружение:
   ```bash
   py -3.10 -m venv venv
   source venv\Scripts\activate  # Для Linux: venv/bin/activate
   ```
4. Установите зависимости из файла requirements.txt:
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. Примените миграции:
   ```bash
   alembic upgrade head
   ```
6. Добавить и настроить файл .env в корневой директории проекта:
    ```bash
    nano .env
    ```
    Пример .env:
    ```
    APP_TITLE=<your_title>
    DESCRIPTION=<your_description>
    DATABASE_URL=<your_database_url>
    SECRET=<your_secret_key>
    ```
6. Запустите сервер:
   ```bash
   uvicorn app.main:app --reload
   ```

## 🧪 Примеры запросов к API

### Создать проект (только суперюзер)
```http
POST /charity_project/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Кошачья клиника",
  "description": "Фонд на операцию",
  "full_amount": 10000
}
```

### Получить список проектов
```http
GET /charity_project/
```

### Обновить проект (только суперюзер)
```http
PATCH /charity_project/1
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "full_amount": 12000
}
```

### Удалить проект (только суперюзер)
```http
DELETE /charity_project/1
Authorization: Bearer <access_token>
```

### Создать пожертвование
```http
POST /donation/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "full_amount": 5000
}
```

### Получить свои пожертвования
```http
GET /donation/my
Authorization: Bearer <access_token>
```

### Получить все пожертвования (только суперюзер)
```http
GET /donation/
Authorization: Bearer <access_token>
```

### Получить аналитику по закрытым проектам (только суперюзер)
```http
POST /google/
Authorization: Bearer <access_token>
```

## Авторизация

Аутентификация реализована через JWT-токены. Для получения токена используйте `/auth/jwt/login`, а для регистрации — `/auth/register`.

## Документация API

После запуска приложение доступно по адресу:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Разработка и тестирование

Для запуска тестов:
```bash
pytest
```

## 🔧 Технологии

- **Python 3.10+**
- **FastAPI** — веб-фреймворк для создания API
- **SQLAlchemy** + **AsyncSession** — асинхронная работа с БД
- **Alembic** — миграции базы данных
- **SQLite** — БД по умолчанию (можно изменить на PostgreSQL и др.)
- **Pydantic** — валидация данных
- **Uvicorn** — ASGI сервер
- **Aiogoogle** — Ассинхронная бабота с GoogleAPI
