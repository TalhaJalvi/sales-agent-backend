"""Discovery routes — find new target companies online."""

import logging

from fastapi import APIRouter
from pydantic import BaseModel

from services.ai_service import extract_companies_from_page
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
    query_parts = [body.industry, "companies"]
    if body.country:
        query_parts.append(body.country)
    if body.keywords:
        query_parts.append(body.keywords)
    query = " ".join(query_parts)

    # Search the web
    search_results = search_web(query, max_results=body.max_results)

    # For each search result, scrape and extract individual companies
    companies = []
    seen_names = set()

    for result in search_results:
        try:
            scraped = scrape_website(result["url"])
            combined_text = f"Source URL: {result['url']}\n\n"
            combined_text += "\n\n".join(p["text"] for p in scraped["pages"])
            combined_text = combined_text[:10000]
            extracted = extract_companies_from_page(combined_text)

            for company in extracted:
                name_lower = company.get("name", "").lower()
                if name_lower and name_lower not in seen_names:
                    seen_names.add(name_lower)
                    companies.append({
                        "name": company.get("name"),
                        "website": company.get("website"),
                        "description": company.get("description"),
                        "industry": company.get("industry"),
                        "country": company.get("country"),
                        "source_url": result["url"],
                    })
        except Exception as e:
            logger.error("Failed to scrape/extract %s: %s", result["url"], e)

    return {"query": query, "results": companies}
