from fastapi import APIRouter, Depends, HTTPException
from db.model import Product, Offer
from db.db_con import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.parsers import parse_data
import httpx
from app.repo import Repo


router = APIRouter(prefix="/products")


@router.post("/")
async def parse_product(db: AsyncSession = Depends(get_db)):
    try:
        data, offers_data = await parse_data()
        obj = Product(**data)
        repo = Repo(session=db)
        res = await repo.add_product(obj)

        offers_obj = [Offer(**{**offer, "product_id": res.id}) for offer in offers_data]
        res_offers = await repo.add_offers(offers_obj)
        await db.commit()
        return {
            "result": res,
            "offers": res_offers
        }
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="seed.json not found")
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing key in seed.json: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
















