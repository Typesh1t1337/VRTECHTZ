import json
from urllib.parse import urlparse


def load_seed(file_path: str):
    with open(file=file_path, mode="r", encoding="utf-8") as f:
        return json.load(f)


def extract_slug(url: str) -> str:
    path = urlparse(url).path
    return path.split("/")[3].split("-")[-1]