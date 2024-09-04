# src/celery_app.py

from celery import Celery
from src.core.config import settings

celery_app = Celery(
    "image_tasks",
    broker=f"amqp://{settings.RABBITMQ_DEFAULT_USER}:{settings.RABBITMQ_DEFAULT_PASSWORD}@rabbitmq:5672/",
    backend="rpc://",
)


# celery_app.conf.update(
#     task_routes={
#         "src.tasks.definitions.process_image": "image_tasks",
#     },
#     task_serializer="json",
#     result_serializer="json",
#     accept_content=["json"],
# )

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)

celery_app.autodiscover_tasks(['src.tasks.definitions.process_image'])