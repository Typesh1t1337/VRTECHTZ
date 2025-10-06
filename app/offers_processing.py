
def process_offer_pages(responses: list) -> tuple[list[dict], int, int]:
    result_to_dump = []
    for page_response in responses:
        for offer in page_response.json()["offers"]:
            result_to_dump.append({"seller": offer["merchantName"], "price": offer["price"]})

    min_price = responses[0].json()["offers"][0]["price"] if responses else 0
    max_price = responses[-1].json()["offers"][-1]["price"] if responses else 0
    return result_to_dump, min_price, max_price
