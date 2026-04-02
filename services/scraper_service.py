"""Playwright-based website scraper."""

import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

from playwright.sync_api import sync_playwright

DATA_DIR = Path(__file__).parent.parent / "data" / "scraped"


def _clean_text(html_text: str) -> str:
    """Strip excessive whitespace from extracted text."""
    text = re.sub(r"\s+", " ", html_text)
    return text.strip()


def _discover_subpages(base_url: str, page) -> list[str]:
    """Find relevant subpages like /about, /team, /products from the homepage."""
    keywords = ["about", "team", "people", "leadership", "products", "services", "solutions"]
    links = page.eval_on_selector_all(
        "a[href]",
        "els => els.map(e => e.getAttribute('href'))",
    )
    found = set()
    parsed_base = urlparse(base_url)
    for href in links:
        if not href:
            continue
        full_url = urljoin(base_url, href)
        parsed = urlparse(full_url)
        # Only same-domain links
        if parsed.netloc != parsed_base.netloc:
            continue
        path_lower = parsed.path.lower().strip("/")
        if any(kw in path_lower for kw in keywords):
            found.add(full_url)
    return list(found)[:5]  # cap at 5 subpages


def scrape_website(url: str, company_id: int | None = None) -> dict:
    """
    Scrape a website and its key subpages.

    Returns dict with:
        - url: the original URL
        - pages: list of {url, text} for each scraped page
    """
    result = {"url": url, "pages": []}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        # Scrape main page
        page.goto(url, wait_until="domcontentloaded", timeout=15000)
        main_text = _clean_text(page.inner_text("body"))
        result["pages"].append({"url": url, "text": main_text})

        # Discover and scrape subpages
        subpages = _discover_subpages(url, page)
        for sub_url in subpages:
            try:
                page.goto(sub_url, wait_until="domcontentloaded", timeout=10000)
                text = _clean_text(page.inner_text("body"))
                result["pages"].append({"url": sub_url, "text": text})
            except Exception:
                continue  # skip failed subpages

        browser.close()

    # Save to disk if company_id provided
    if company_id is not None:
        save_path = DATA_DIR / str(company_id)
        save_path.mkdir(parents=True, exist_ok=True)
        file_path = save_path / "scraped.json"
        file_path.write_text(json.dumps(result, indent=2))
        return {**result, "saved_path": str(file_path)}

    return result
