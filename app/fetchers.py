import httpx
import asyncio


async def fetch_html(client: httpx.AsyncClient, url: str, headers: dict) -> httpx.Response:
    return await client.get(url, headers=headers)


async def fetch_offer_page(client: httpx.AsyncClient, slug: str, page: int, limit: int, body: dict, headers: dict) -> httpx.Response:
    new_body = body.copy()
    new_body["page"] = page
    new_body["limit"] = limit
    return await client.post(f"https://kaspi.kz/yml/offer-view/offers/{slug}", headers=headers, json=new_body)


async def fetch_reviews(client: httpx.AsyncClient, slug: str, headers: dict) -> httpx.Response:
    return await client.get(
        f"https://kaspi.kz/yml/review-view/api/v1/reviews/product/{slug}?baseProductCode&orderCode&filter=COMMENT&sort=POPULARITY&limit=9&merchantCodes&withAgg=true",
        headers=headers
    )
