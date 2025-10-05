from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Numeric, Float, ARRAY, ForeignKey, DateTime
from decimal import Decimal
from sqlalchemy.dialects.postgresql import JSONB


Base = declarative_base()


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    category: Mapped[str] = mapped_column(String, index=True, nullable=False)
    min_price: Mapped[Decimal] = mapped_column(Numeric(scale=2), nullable=False)
    max_price: Mapped[Decimal] = mapped_column(Numeric(scale=2), nullable=False)
    rate: Mapped[Float] = mapped_column(Float, nullable=False)
    review_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    seller_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    image_url: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    characteristic: Mapped[dict] = mapped_column(JSONB, nullable=False)

    price_history: Mapped[list["ProductHistory"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
    )


class ProductHistory(Base):
    __tablename__ = 'product_history'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(scale=2), nullable=False)
    checked_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    product: Mapped["Product"] = relationship(back_populates="history")
