import os
import requests
from typing import List, Dict
from dotenv import load_dotenv
load_dotenv()


class MediastackFetcher:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("MEDIASTACK_KEY")
        self.base = "http://api.mediastack.com/v1/news"

    def fetch(self, keywords: str = "technology", limit: int = 5) -> List[Dict]:
        if not self.api_key:
            return []
        params = {"access_key": self.api_key, "keywords": keywords, "limit": limit}
        try:
            r = requests.get(self.base, params=params, timeout=12)
            r.raise_for_status()
            data = r.json().get("data", [])
            return [
                {
                    "title": a.get("title"),
                    "description": a.get("description"),
                    "url": a.get("url"),
                    "published_at": a.get("published_at"),
                    "source": a.get("source"),
                    "raw": a
                }
                for a in data
            ]
        except Exception as e:
            print("Mediastack fetch error:", e)
            return []

class GNewsFetcher:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GNEWS_KEY")
        self.base = "https://gnews.io/api/v4/search"

    def fetch(self, q: str = "technology", max_results: int = 5) -> List[Dict]:
        if not self.api_key:
            return []
        params = {"token": self.api_key, "q": q, "max": max_results, "lang": "en"}
        try:
            r = requests.get(self.base, params=params, timeout=12)
            r.raise_for_status()
            data = r.json().get("articles", [])
            return [
                {
                    "title": a.get("title"),
                    "description": a.get("description"),
                    "url": a.get("url"),
                    "published_at": a.get("publishedAt"),
                    "source": a.get("source", {}).get("name"),
                    "raw": a
                }
                for a in data
            ]
        except Exception as e:
            print("GNews fetch error:", e)
            return []
