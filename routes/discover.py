"""Discovery routes — find new target companies online."""

import logging

from fastapi import APIRouter
from pydantic import BaseModel

from services.ai_service import extract_company_info
from services.scraper_service import scrape_website
from services.search_service import search_web

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/discover", tags=["discover"])


class DiscoverBody(BaseModel):
    industry: str
    country: str | None = None
    keywords: str | None = None
    max_results: int = 5


@router.post("/")
def discover_companies(body: DiscoverBody):
    # Build search query
    query_parts = [body.industry, "company"]
    if body.country:
        query_parts.append(body.country)
    if body.keywords:
        query_parts.append(body.keywords)
    query = " ".join(query_parts)

    # Search the web
    search_results = search_web(query, max_results=body.max_results)

    # For each result, try to scrape and extract basic info
    discoveries = []
    for result in search_results:
        entry = {
            "url": result["url"],
            "title": result["title"],
            "snippet": result["snippet"],
            "extracted": None,
            "error": None,
        }
        try:
            scraped = scrape_website(result["url"])
            combined_text = "\n\n".join(p["text"] for p in scraped["pages"])
            combined_text = combined_text[:10000]
            extracted = extract_company_info(combined_text)
            entry["extracted"] = extracted
        except Exception as e:
            logger.error("Failed to scrape/extract %s: %s", result["url"], e)
            entry["error"] = str(e)

        discoveries.append(entry)

    return {"query": query, "results": discoveries}
