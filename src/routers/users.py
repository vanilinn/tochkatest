from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from jose import jwt, JWTError

from src.schemas.users import UserCreate, User, Token
from src.core.database import get_async_session
from src.core.config import settings
from src.cruds.cruds import user_crud
from src.services.dependencies import get_current_user
from src.services.services import create_access_token

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


@router.post("/register/", response_model=User)
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    existing_user = await user_crud.get_by_attribute(session=session, email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.password = get_password_hash(user.password)
    return await user_crud.create(user, session)


@router.post("/login/", response_model=Token)
async def login_user(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    db_user = await user_crud.get_by_attribute(session=session, email=user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = await create_access_token(data={"sub": db_user.email})
    return {"token": access_token}


@router.get("/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
