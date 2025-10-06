import json
from bs4 import BeautifulSoup
import re


def extract_product_data_from_scripts(html_text: str) -> dict:
    soup = BeautifulSoup(html_text, "html.parser")
    scripts = soup.find_all("script", type="application/ld+json")
    for script in scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, dict) and "description" in data:
                return data
        except (json.JSONDecodeError, TypeError):
            continue
    return {}


def extract_images(html_text: str) -> list[str]:
    no_type_scripts = html_text.split("</script><script>")[9]
    match = re.search(r'BACKEND\.components\.item\s*=\s*(\{.*\});?', no_type_scripts, re.DOTALL)
    images = []
    if match:
        json_str = match.group(1)
        gallery = json.loads(json_str).get("galleryImages", [])
        for img_dict in gallery:
            for k, v in img_dict.items():
                if k == "large":
                    images.append(v)
    return images
