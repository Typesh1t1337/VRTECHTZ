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

    async def add__or_update_product(self, product) -> tuple[Product, bool]:
        stmt = select(Product).where(Product.kaspi_id == product.kaspi_id)
        result = await self.session.execute(stmt)
        existing_product = result.scalar_one_or_none()

        if existing_product is not None:
            changed = False
            for field in ["description", "category", "min_price", "max_price", "rate",
                          "review_amount", "seller_amount", "image_url"]:
                new_value = getattr(product, field)
                if getattr(existing_product, field) != new_value:
                    setattr(existing_product, field, new_value)
                    changed = True

            if changed:
                await self.session.flush()
            return existing_product, changed
        else:
            self.session.add(product)
            await self.session.flush()
            return product, True

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
