from datetime import datetime
from jose import JWTError, jwt
from typing import Optional

from fastapi import Depends, HTTPException, status, Request, WebSocket, Security
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
    OAuth2
)
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from os import environ
from dotenv import load_dotenv

from src.services import services
from src.schemas.users import User, TokenData
from src.core.config import settings
from src.cruds import user_crud
from src.core.database import get_async_session

load_dotenv()


security = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/login")


async def get_current_user(
        token: str = Depends(security),
        session: AsyncSession = Depends(get_async_session)

):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, str(settings.SECRET_KEY), algorithms=["HS256"])
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except (JWTError, ValidationError):
        raise credentials_exception

    user = await user_crud.get_by_attribute(session=session, email=token_data.email)

    if not user:
        raise credentials_exception
    return user
