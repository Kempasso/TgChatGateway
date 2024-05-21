from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import typing


@dataclass
class BaseMixin:
    table: typing.Any
    session: AsyncSession


class GetMixin(BaseMixin):
    async def first_instance_by_values(self, **kwargs):
        instance = select(self.table).filter_by(**kwargs)
        result = await self.session.execute(instance)
        return result.scalars().first()


class CreateMixin(BaseMixin):

    async def create(self, **kwargs):
        instance = self.table(**kwargs)
        self.session.add(instance)
        instance = await self.session.commit()
        return instance

    async def get_or_create(self, defaults=None, **kwargs):
        query = select(self.table).filter_by(**kwargs)
        instance = await self.session.execute(query)
        instance = instance.scalars().first()
        if instance:
            return instance
        data = dict(**kwargs)
        if defaults:
            data.update(defaults)
        instance = self.table(**data)
        self.session.add(instance)
        instance = await self.session.commit()
        return instance

# :TODO
class UpdateMixin(BaseMixin):
    pass

# :TODO
class FilterMixin(BaseMixin):
    pass
