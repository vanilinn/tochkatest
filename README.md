# Image Processing API

## Описание

Этот проект представляет собой API для обработки изображений с использованием FastAPI и Celery. Пользователи могут загружать изображения, и API выполняет над ними различные трансформации, такие как поворот, преобразование в черно-белый формат и изменение масштаба. Проект использует Docker для контейнеризации и PostgreSQL для хранения данных.

## Установка

### Предварительные требования

- Python 3.11+
- Docker
- Docker Compose

### Шаги установки

1. **Клонируйте репозиторий:**

    ```bash
    git clone https://github.com/yourusername/yourproject.git
    cd yourproject
    ```

2. **Создайте и активируйте виртуальное окружение:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Windows используйте `venv\Scripts\activate`
    ```

3. **Установите зависимости:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Настройте файлы конфигурации:**

    Скопируйте пример конфигурационного файла и измените его при необходимости:

    ```bash
    cp .env.example .env
    ```

5. **Запустите проект с использованием Docker Compose:**

    ```bash
    docker-compose up --build
    ```

## Использование

### Запуск сервера

После запуска Docker Compose сервер FastAPI будет доступен по адресу [http://localhost:8000](http://localhost:8000).

### Загрузка изображения

Отправьте POST-запрос на `/api/v1/upload/` с изображением в теле запроса. В ответ вы получите ID задачи, который можно использовать для проверки статуса задачи.

Пример запроса:

```bash
curl -X POST "http://localhost:8000/api/v1/upload/" -F "file=@/path/to/your/image.jpg"
