from typing import Sequence
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from db.model import Product, Offer
from sqlalchemy import select


class Repo:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def add_product(self, product) -> Product:
        self.session.add(product)
        await self.session.flush()

        return product

    async def add_offers(self, offers) -> Offer:
        self.session.add_all(offers)
        await self.session.flush()

        return offers

    async def get_products(self) -> Sequence[Product]:
        stmt = select(Product).options(selectinload(Product.offers))
        query = await self.session.execute(stmt)
        result = query.scalars().all()

        return result
