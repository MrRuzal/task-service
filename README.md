# Task Service

### Описание
Этот проект представляет собой простой Django-проект, для асинхронного выполнения задач.

### Используемые технологии
- Python 3.11
- Django 4.2
- Django REST Framework 3.14
- PostgreSQL 15.2
- Docker
- Redis
- Celery

### Установка
1. Убедитесь, что у вас установлен Docker и Docker Compose.
2. Склонируйте репозиторий:

    ```bash
    git clone https://github.com/devbkd/task-service.git
    ```
3. Перейдите в каталог проекта:

    ```bash
    cd task-service
    ```
4. Запустите контейнеры:

    ```bash
    docker-compose up --build
    ```
5. Создайте суперпользователя (если нужно):

    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```
6. Откройте веб-приложение в браузере: [http://localhost:8000](http://localhost:8000)

### Использование
Создание задачи через админ-панель:
1. Перейдите в админ-панель: http://localhost:8000/admin/
2. Войдите, используя учетные данные созданного суперпользователя.
3. Перейдите в раздел "Tasks" и создайте новую задачу, указав номер и статус "created".

Создание пользователя и задачи через API нужно перейти в документацию http://127.0.0.1:8000/redoc/ или http://127.0.0.1:8000/swagger/ . Так же через API можно добавлять пользователей, получать токены.  

Выполнения задач можно просматривать в Celery Flower http://localhost:5555/

Для проверки работоспособности время отработки указаны не большие. 
При необходимости их нужно изменить в файлах celery.py и tasks.py  
`DELETE_OLD_TASKS_SCHEDULE = timedelta(minutes=10)`  
`RETRY_STUCK_TASKS_SCHEDULE = timedelta(minutes=1)`  
`OLD_TASKS_THRESHOLD = timedelta(minutes=10)`

## Автор:
Рузал Закиров [GitHub](https://github.com/devbkd/)