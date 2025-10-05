from repo import Repo
from sqlalchemy.ext.asyncio import AsyncSession


class Service:
    def __init__(self, repo: Repo, session: AsyncSession):
        self.repo = repo
        self.session = session

    async def create_product(self):
        pass



