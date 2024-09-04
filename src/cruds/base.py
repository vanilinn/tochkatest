from sqlalchemy import select, update, false
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:

    def __init__(self, model):
        self.__model = model

    async def get_by_attribute(
            self,
            session: AsyncSession,
            **param
    ):
        obj = await session.scalars(select(self.__model).filter_by(**param))
        o = obj.first()
        return o if o else {}

    async def get_all(
            self,
            session: AsyncSession,
            **param
    ):
        objs = await session.scalars(select(self.__model).filter_by(**param))
        return objs.all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
    ):
        obj_in_data = obj_in.dict()
        obj = self.__model(**obj_in_data)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def update(
            self,
            obj,
            obj_in,
            session: AsyncSession,
            **param
    ):
        update_data = obj_in.dict(exclude_unset=True)
        await session.execute(
            update(self.__model).filter_by(id=obj.id, **param).values(**update_data)
        )
        await session.commit()
        await session.refresh(obj)
        return obj

    @staticmethod
    async def remove(
            obj,
            session: AsyncSession
    ):
        await session.delete(obj)
        await session.commit()
        return obj
