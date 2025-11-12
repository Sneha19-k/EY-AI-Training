from difflib import SequenceMatcher
from typing import List, Dict

def is_similar(a: str, b: str, threshold: float = 0.86) -> bool:
    if not a or not b:
        return False
    return SequenceMatcher(None, a, b).ratio() > threshold

def dedupe_articles(articles: List[Dict]) -> List[Dict]:
    """
    Simple de-duplication by title similarity and exact URL match.
    Newer-first ordering preserved if 'published_at' is present.
    """
    # Sort by published_at if available, newest first
    def key_fn(x):
        return x.get("published_at") or ""
    articles_sorted = sorted(articles, key=key_fn, reverse=True)
    unique = []
    urls = set()
    for a in articles_sorted:
        url = a.get("url")
        if url and url in urls:
            continue
        # check title similarity
        title = a.get("title", "")
        if any(is_similar(title, u.get("title", "")) for u in unique):
            continue
        unique.append(a)
        if url:
            urls.add(url)
    return unique
