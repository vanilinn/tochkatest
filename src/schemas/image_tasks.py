from pydantic import BaseModel, Field
from typing import Optional, List


class ImageTaskResponse(BaseModel):
    task_id: str = Field(..., description="ID задачи в Celery")
    status: str = Field(..., description="Статус выполнения задачи")
    result: Optional[str] = Field(None,
                                  description="Результат обработки изображения (ссылка на обработанное изображение)")

    class Config:
        orm_mode = True


class ImageTaskResponse1(BaseModel):
    task_id: str
    status: str
    result: Optional[List[str]]  # Измените это на список строк, а не строку
