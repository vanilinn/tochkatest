import logging
import os
import uvicorn

from dotenv import load_dotenv

from fastapi import FastAPI, Depends, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from src.routers import users, image_tasks
from src.core.config import settings

load_dotenv()
# locale.setlocale(locale.LC_ALL, "ru")

description = """
# IMAGE AUGMENTATION API
## Для начала работы в Swagger, необходимо нажать на кнопку Authorize и ввести логин и пароль.
"""

app = FastAPI(
    title="IMAGE AUGMENTATION API 🚀",
    description=description
)

log = logging.getLogger(__name__)
log_handler = logging.StreamHandler()
log_handler.setFormatter(logging.Formatter("[%(asctime)s] - [%(levelname)s] - [%(message)s]"))
log.addHandler(log_handler)
log.setLevel(logging.INFO)

# work_dir = os.getcwd()
# images_folder = os.path.join(work_dir, os.path.normpath('./images/'))
# log.info(f'\nCurrent dir - {work_dir}\nImages dir {images_folder}\n')

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_PREFIX = settings.API_PREFIX

app.include_router(users.router, prefix=API_PREFIX, tags=['Пользователи'])
app.include_router(image_tasks.router, prefix=API_PREFIX, tags=['Задачи для изображений'])


@app.get('/api/healthchecker')
def root():
    return {'message': 'OK!'}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
