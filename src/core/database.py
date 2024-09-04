import uuid

from sqlalchemy import MetaData, exc, Column, Integer, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import Session, sessionmaker, declared_attr, Mapped, mapped_column, DeclarativeBase

from .config import settings

convention = {
    "all_column_names": lambda constraint, table: "_".join(
        [column.name for column in constraint.columns.values()]
    ),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
    "pk": "pk__%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=convention)  # type: ignore

    @declared_attr
    def __tablename__(cls):
        return f'{cls.__name__.lower()}s'

    id: Mapped[uuid] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)


DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
        except exc.SQLAlchemyError as error:
            await session.rollback()
            raise
        finally:
            await session.close()
