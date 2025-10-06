import asyncio
import json
from urllib.parse import urlparse

from app.fetchers import fetch_html, fetch_offer_page, fetch_reviews
from app.parsers_html import extract_product_data_from_scripts, extract_images
from app.offers_processing import process_offer_pages
from app.utils import save_json_file
import httpx


async def parse_data() -> tuple[dict, list[dict]]:
    with open("seed.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    url = data["product_url"]
    path = urlparse(url).path
    slug = path.split("/")[3].split("-")[-1]

    body = {
        "cityId": "750000000",
        "id": "106185651",
        "limit": 1,
        "page": 0,
        "sortOption": "PRICE",
        "highRating": None,
        "searchText": None,
        "isExcellentMerchant": None,
        "installationId": "-1"
    }

    headers_api = {
        "Content-Type": "application/json; charset=UTF-8",
        "Host": "kaspi.kz",
        "Referer": url,
        "Origin": "https://kaspi.kz",
        "User-Agent": "PostmanRuntime/7.48.0"
    }

    headers_html = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/118.0.5993.90 Safari/537.36",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    async with httpx.AsyncClient() as client:
        # HTML, офферы первой страницы и отзывы
        response_html, response_offer_api, response_review_api = await asyncio.gather(
            fetch_html(client, url, headers_html),
            fetch_offer_page(client, slug, page=0, limit=1, body=body, headers=headers_api),
            fetch_reviews(client, slug, headers=headers_api)
        )

        product_data = extract_product_data_from_scripts(response_html.text)
        images = extract_images(response_html.text)

        result_offer_api = response_offer_api.json()
        result_review_api = response_review_api.json()
        total_offers = result_offer_api["offersCount"]
        rate = result_review_api["summary"]["global"]
        review_amount = result_review_api["groupSummary"][1]["total"]

        pages_to_parse = (total_offers + 63) // 64 - 1
        tasks = [fetch_offer_page(client, slug, i, 64, body, headers_api) for i in range(pages_to_parse + 1)]
        responses = await asyncio.gather(*tasks)

        offers, min_price, max_price = process_offer_pages(responses)

        # Папка для экспорта
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
        export_folder = os.path.join(parent_dir, "export")

        save_json_file(export_folder, "offers.json", offers)

        result = {
            "kaspi_id": int(slug),
            "name": product_data["name"],
            "description": product_data["description"],
            "category": product_data["category"],
            "image_url": images,
            "min_price": min_price,
            "max_price": max_price,
            "review_amount": review_amount,
            "rate": rate,
            "seller_amount": total_offers,
        }

        save_json_file(export_folder, "export.json", result)

        return result, offers
