import asyncio
import os
from urllib.parse import urlparse
import json
import httpx
from bs4 import BeautifulSoup
from fastapi import HTTPException


async def parse_data():
    with open(file="seed.json", mode="r", encoding="utf-8") as f:
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
        response_html, response_offer_api, response_review_api = await asyncio.gather(
            client.get(url, headers=headers_html),
            client.post(f"https://kaspi.kz/yml/offer-view/offers/{slug}", headers=headers_api, json=body),
            client.get(
                f"https://kaspi.kz/yml/review-view/api/v1/reviews/product/{slug}?baseProductCode&orderCode&filter=COMMENT&sort=POPULARITY&limit=9&merchantCodes&withAgg=true",
                headers=headers_api
            )
        )

        soup = BeautifulSoup(response_html.text, "html.parser")
        scripts = soup.find_all("script", type="application/ld+json")

        product_data = None

        for script in scripts:
            try:
                data_to_find = json.loads(script.string)
                if isinstance(data_to_find, dict) and "description" in data_to_find:
                    product_data = data_to_find
                    break
            except (json.decoder.JSONDecodeError, TypeError):
                continue

        result_offer_api = response_offer_api.json()
        result_review_api = response_review_api.json()
        total_offers = result_offer_api["offersCount"]
        rate = result_review_api["summary"]["global"]
        min_price = result_offer_api["offers"][0]["price"]
        review_amount = result_review_api["groupSummary"][1]["total"]

        new_api_body = body.copy()
        new_api_body["page"] = total_offers - 1

        response = await client.post(url=f"https://kaspi.kz/yml/offer-view/offers/{slug}", headers=headers_api,
                                         json=new_api_body)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        response_json = response.json()

        max_price = response_json["offers"][0]["price"]
        each_page_responses = []

        pages_to_parse = (total_offers + 63) // 64 - 1
        for i in range(pages_to_parse + 1):
            new_api_body = body.copy()
            new_api_body["page"] = i
            new_api_body["limit"] = 64
            response = client.post(f"https://kaspi.kz/yml/offer-view/offers/{slug}", headers=headers_api, json=new_api_body)
            each_page_responses.append(response)

        responses = await asyncio.gather(*each_page_responses)
        result_to_dump = dict()

        for each_page_response in responses:
            each_page_response_json = each_page_response.json()
            for offer in each_page_response_json["offers"]:
                result_to_dump[offer["merchantName"]] = offer["price"]

        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.abspath(os.path.join(current_dir, ".."))

        new_folder = os.path.join(parent_dir, "export")

        os.makedirs(new_folder, exist_ok=True)
        with open(os.path.join(new_folder, "offers.json"), "w", encoding="utf-8") as f:
            f.write(json.dumps(result_to_dump, ensure_ascii=False, indent=4))

        result = {
            "name": product_data["name"],
            "description": product_data["description"],
            "category": product_data["category"],
            "image": product_data["image"],
            "min_price": min_price,
            "max_price": max_price,
            "review_amount": review_amount,
            "rate": rate,
        }

        with open(f"{new_folder}/export.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(result, ensure_ascii=False, indent=4))

        return result