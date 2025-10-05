from sqlalchemy.ext.asyncio import AsyncSession
from db.model import Product


class Repo:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def add_product(self, product: Product) -> Product:
        self.session.add(product)
        await self.session.flush()

        return product

