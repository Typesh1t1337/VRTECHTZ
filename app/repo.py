from typing import Sequence

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from db.model import Product, Offer, ProductHistory
from sqlalchemy import select


class Repo:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def add_product(self, product) -> Product | None:
        try:
            self.session.add(product)
            await self.session.flush()

            return product
        except IntegrityError as e:
            await self.session.rollback()
            if "uq_product_full_duplicate" in str(e.orig):
                raise HTTPException(status_code=400, detail="Duplicate entry detected")
            raise

    async def add_offers(self, offers) -> list[Offer]:
        self.session.add_all(offers)
        await self.session.flush()

        return offers

    async def get_products(self) -> Sequence[Product]:
        stmt = select(Product).options(selectinload(Product.offers))
        query = await self.session.execute(stmt)
        result = query.scalars().all()

        return result

    async def get_products_history(self) -> Sequence[Product]:
        stmt = select(Product).options(selectinload(Product.product_history), selectinload(Product.offers_history))
        query = await self.session.execute(stmt)
        result = query.scalars().all()

        return result
