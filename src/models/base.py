from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class BaseModel(Base):

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
