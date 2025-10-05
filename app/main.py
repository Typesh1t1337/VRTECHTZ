from fastapi import FastAPI
from app.api import router
from db.model import Base
from db.db_con import engine


class AppFactory:
    def __init__(self):
        self.app = FastAPI()
        self.app.add_event_handler("startup", self.on_startup)
        self.add_routes()

    def add_routes(self):
        self.app.include_router(router)

    @staticmethod
    async def on_startup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


app = AppFactory().app
