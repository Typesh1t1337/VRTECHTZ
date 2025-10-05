import httpx


async def fetch_html(client: httpx.AsyncClient, url: str):
    headers_html = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/118.0.5993.90 Safari/537.36",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    response = await client.get(url, headers=headers_html)
    response.raise_for_status()
    return response.text


async def fetch_offers_page(client: httpx.AsyncClient, slug: str, page: int, limit: int = 64):
    headers_api = {
        "Content-Type": "application/json; charset=UTF-8",
        "Host": "kaspi.kz",
        "Referer": f"https://kaspi.kz/shop/p/{slug}",
        "Origin": "https://kaspi.kz",
        "User-Agent": "PostmanRuntime/7.48.0"
    }
    body = {
        "cityId": "750000000",
        "id": "106185651",
        "limit": limit,
        "page": page,
        "sortOption": "PRICE",
        "highRating": None,
        "searchText": None,
        "isExcellentMerchant": None,
        "installationId": "-1"
    }
    response = await client.post(
        f"https://kaspi.kz/yml/offer-view/offers/{slug}",
        headers=headers_api,
        json=body
    )
    response.raise_for_status()
    return response.json()


async def fetch_reviews(client: httpx.AsyncClient, slug: str):
    headers_api = {
        "Content-Type": "application/json; charset=UTF-8",
        "Host": "kaspi.kz",
        "Referer": f"https://kaspi.kz/shop/p/{slug}",
        "Origin": "https://kaspi.kz",
        "User-Agent": "PostmanRuntime/7.48.0"
    }
    url = (f"https://kaspi.kz/yml/review-view/api/v1/reviews/product/{slug}"
           "?baseProductCode&orderCode&filter=COMMENT&sort=POPULARITY&limit=9&merchantCodes&withAgg=true")
    response = await client.get(url, headers=headers_api)
    response.raise_for_status()
    return response.json()

