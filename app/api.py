from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status

from db.model import Product, Offer
from db.db_con import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.tools import parse_data
import httpx
from app.repo import Repo
from app.schema import ProductResponse, ProductWithHistoryResponse


router = APIRouter(prefix="/products")


@router.post("/")
async def parse_product(db: AsyncSession = Depends(get_db)):
    try:
        data, offers_data = await parse_data()
        obj = Product(**data)
        repo = Repo(session=db)
        res, changed = await repo.add__or_update_product(obj)
        if not changed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product exist and not updated"
            )

        offers_obj = [Offer(**{**offer, "product_id": res.id}) for offer in offers_data]
        res_offers = await repo.add_offers(offers_obj)
        await db.commit()
        return {
            "result": res,
            "offers": res_offers
        }
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="seed.json not found")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.get("/", response_model=list[ProductResponse])
async def get_products(db: AsyncSession = Depends(get_db)):
    repo = Repo(session=db)
    res = await repo.get_products()

    return res


@router.get("/history", response_model=list[ProductWithHistoryResponse])
async def get_history(db: AsyncSession = Depends(get_db)):
    repo = Repo(session=db)
    res = await repo.get_products_history()

    return res




