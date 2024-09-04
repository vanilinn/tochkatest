from src.models.models import User, ImageTask
from .base import CRUDBase

user_crud = CRUDBase(User)
image_crud = CRUDBase(ImageTask)
