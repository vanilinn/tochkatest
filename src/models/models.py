import uuid

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from src.models.base import BaseModel


class User(BaseModel):
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=True)

    def __repr__(self):
        return f'Пользователь: {self.email}'


class ImageTask(BaseModel):
    task_id: Mapped[uuid] = mapped_column(UUID(as_uuid=True), nullable=True)
    img_link: Mapped[str] = mapped_column(Text, nullable=True)
    user: Mapped[uuid] = mapped_column(UUID, ForeignKey("users.id"))

    def __repr__(self):
        return f'Image task: {self.task_id}'
