from sqlalchemy.ext.asyncio import AsyncSession
from celery_app.celery import celery_app
from app.tools import parse_data
import asyncio
from sqlalchemy import select
from db.db_con import async_session
from db.model import Product, ProductHistory, Offer, OfferHistory
from celery_app.celery_logger import get_logger


@celery_app.task
def update_products():
    logger = get_logger()
    try:
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(update_all_products(logger))
        loop.run_until_complete(future)
        logger.info("Celery task 'update_products' started")
    except RuntimeError:
        asyncio.run(update_all_products(logger))


async def update_all_products(logger):
    data, offers_data = await parse_data()

    async with async_session() as session:
        stmt = select(Product).where(Product.kaspi_id == data['kaspi_id'])
        query = await session.execute(stmt)
        db_product = query.scalars().first()

        if db_product:
            changed = False
            changes = {}

            for field in ["description", "category", "min_price", "max_price", "rate", "review_amount",
                          "seller_amount"]:
                if getattr(db_product, field) != data[field]:
                    changes[field] = {"old": getattr(db_product, field), "new": data[field]}
                    changed = True
                    break

            if changed:
                history = ProductHistory(
                    product_id=db_product.id,
                    name=db_product.name,
                    description=db_product.description,
                    category=db_product.category,
                    min_price=db_product.min_price,
                    max_price=db_product.max_price,
                    rate=db_product.rate,
                    review_amount=db_product.review_amount,
                    seller_amount=db_product.seller_amount,
                )
                session.add(history)
                logger.info({"type": "product_update", "product_id": db_product.id, "changes": changes})

                for field in ["description", "category", "min_price", "max_price", "rate", "review_amount",
                              "seller_amount"]:
                    setattr(db_product, field, data[field])

        else:
            db_product = Product(**data)
            session.add(db_product)
            await session.flush()
            logger.info({"type": "product_added", "product_id": db_product.id})

        stmt = select(Offer).where(Offer.product_id == db_product.id)
        query = await session.execute(stmt)
        existing_offers = query.scalars().all()

        existing_map = {o.seller: o for o in existing_offers}

        new_offers = []
        offers_history = []

        for offer_data in offers_data:
            seller = offer_data["seller"]
            db_offer = existing_map.get(seller)

            if db_offer:
                if db_offer.price != offer_data["price"]:
                    history = OfferHistory(
                        offer_id=db_offer.id,
                        product_id=db_offer.product_id,
                        seller=db_offer.seller,
                        price=db_offer.price,
                    )

                    offers_history.append(history)

                    db_offer.price = offer_data["price"]
            else:
                new_offer = Offer(product_id=db_product.id, **offer_data)
                new_offers.append(new_offer)

        if new_offers:
            session.add_all(new_offers)
        if offers_history:
            session.add_all(offers_history)

        await session.commit()
        logger.info({"type": "task_finished", "product_id": db_product.id})










