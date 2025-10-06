from sqlalchemy.ext.asyncio import AsyncSession
from db.model import Product, Offer


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

