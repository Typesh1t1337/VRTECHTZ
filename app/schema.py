from pydantic import BaseModel, ConfigDict
from decimal import Decimal


class OfferResponse(BaseModel):
    id: int
    seller: str
    price: Decimal

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True
    )


class ProductResponse(BaseModel):
    id: int
    description: str
    category: str
    min_price: Decimal
    max_price: Decimal
    rate: float
    kaspi_id: int
    review_amount: int
    seller_amount: int
    image_url: list[str]
    offers: list[OfferResponse]