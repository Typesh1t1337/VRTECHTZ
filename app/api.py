from fastapi import APIRouter, Depends, HTTPException
from db.model import Product
from db.db_con import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.parsers import parse_data
import httpx


router = APIRouter(prefix="/products")


@router.post("/")
async def parse_product():
    try:
        result = await parse_data()
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="seed.json not found")
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing key in seed.json: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

    return result















