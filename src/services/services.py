import hashlib
import json
import random
import string
from datetime import datetime, timedelta
from enum import Enum

from jose import jwt
from sqlalchemy import desc, func, select, any_

from src.core.config import settings


def get_random_string(length: int = 12) -> str:
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None) -> str:
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str) -> bool:
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed


async def update_item(item: any, item_detail: any, schema: any) -> dict:
    """
    Метод для выборочного обновления полей сущностей
    item - входящий словарь, требующий изменения полей
    item_detail - поля с изменениями значений
    schema - валидация полей
    """
    stored_item_model = schema(**item)
    update_data = item_detail.dict(exclude_unset=True)
    update_item_detail = stored_item_model.copy(update=update_data)
    return update_item_detail


# создание jwt токена
async def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, str(settings.SECRET_KEY), algorithm="HS256")
    return encoded_jwt
