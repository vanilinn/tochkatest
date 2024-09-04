# src/routers/image_tasks.py

import os
import uuid
import zipfile

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from src.celery_app import celery_app
from src.core.database import get_async_session
from src.models.models import ImageTask, User
from src.cruds.cruds import image_crud, user_crud
from src.schemas.image_tasks import ImageTaskResponse, ImageTaskResponse1
from src.services.dependencies import get_current_user

router = APIRouter()

# Папка для сохранения изображений
IMAGE_FOLDER = "images"


@router.post("/upload/", response_model=ImageTaskResponse)
async def upload_image(
        file: UploadFile = File(...),
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(get_current_user)
):
    task_id = str(uuid.uuid4())
    image_filename = f"{task_id}_original.jpg"
    image_path = os.path.join(IMAGE_FOLDER, image_filename)

    with open(image_path, "wb") as image_file:
        image_file.write(await file.read())

    task = celery_app.send_task(
        "src.tasks.definitions.process_image",
        args=[task_id, image_filename, ["rotate", "gray", "scale"]]
    )

    image_task = ImageTask(
        task_id=task.id,
        img_link=image_filename,
        user=current_user.id
    )
    print(1)
    session.add(image_task)
    await session.commit()
    await session.refresh(image_task)
    print(2)
    return ImageTaskResponse(task_id=task.id, status="Processing")


@router.get("/status/{task_id}/", response_model=ImageTaskResponse1)
async def get_task_status(
        task_id: str,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(get_current_user)
):
    task = celery_app.AsyncResult(task_id)

    # Обновите логику для работы с результатом, который теперь является списком путей
    if task.state == "SUCCESS":
        result = task.result
        # Можно вернуть список путей к изображениям
        return {
            "task_id": task_id,
            "status": task.state,
            "result": result
        }

    return {
        "task_id": task_id,
        "status": task.state,
        "result": None
    }


# src/routers/image_tasks.py

@router.get("/history/{user_id}/")
async def get_user_history(
        user_id: str,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    image_tasks = await session.scalars(
        select(ImageTask)
        .options(joinedload(ImageTask.user))
        .filter(ImageTask.user == current_user.id)
    )

    return [{"task_id": task.task_id, "img_link": task.img_link, "created_at": task.created_at} for task in image_tasks]


@router.get("/task/{task_id}/")
async def download_task_images(
        task_id: str,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(get_current_user)
):
    task_images = await session.scalars(
        select(ImageTask)
        .filter_by(task_id=task_id, user_id=current_user.id)
    )

    if not task_images:
        raise HTTPException(status_code=404, detail="No images found for this task")

    zip_filename = f"{task_id}.zip"
    zip_filepath = os.path.join(IMAGE_FOLDER, zip_filename)

    with zipfile.ZipFile(zip_filepath, "w") as zip_file:
        for task_image in task_images:
            image_path = os.path.join(IMAGE_FOLDER, task_image.img_link)
            zip_file.write(image_path, arcname=os.path.basename(image_path))

    return FileResponse(zip_filepath, filename=zip_filename, media_type="application/zip")
