FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /src
COPY . /src
# install psycopg2 dependencies
# RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip
RUN pip install -r /src/requirements.txt --no-cache-dir
EXPOSE 8000
# Запуск команды
#CMD ["celery", "-A", "src.celery_app", "worker", "--loglevel=info"]