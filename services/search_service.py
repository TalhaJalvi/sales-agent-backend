"""DuckDuckGo search wrapper."""

from ddgs import DDGS


def search_web(query: str, max_results: int = 10) -> list[dict]:
    """Search the web and return a list of {title, url, snippet}."""
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_results)
    return [
        {"title": r["title"], "url": r["href"], "snippet": r["body"]}
        for r in results
    ]
