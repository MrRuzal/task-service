FROM python:3.11

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    redis-tools \
    && rm -rf /var/lib/apt/lists/*

CMD celery -A task_service worker -l info -B && gunicorn --bind 0.0.0.0:8000 task_service.wsgi
