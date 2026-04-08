"""Enrichment command — scrape a company website, extract info via AI, save to DB."""

from sqlalchemy.orm import Session

from models import Company, Person, Product
from services.ai_service import extract_company_info
from services.scraper_service import scrape_website


def enrich_company(db: Session, company_id: int) -> Company:
    """Scrape the company's website, extract structured data via AI, and update the DB."""
    company = db.get(Company, company_id)
    if company is None:
        raise ValueError(f"Company {company_id} not found")
    if not company.website:
        raise ValueError(f"Company {company_id} has no website to scrape")

    # 1. Scrape website and subpages
    scraped = scrape_website(company.website, company_id=company_id)

    # 2. Combine all page text for AI extraction
    combined_text = f"Company website: {company.website}\n\n"
    combined_text += "\n\n".join(p["text"] for p in scraped["pages"])
    combined_text = combined_text[:15000]  # truncate to avoid token limits

    # 3. Extract structured info via AI
    extracted = extract_company_info(combined_text)

    # 4. Update company fields
    if extracted.get("description"):
        company.description = extracted["description"]
    if extracted.get("industry"):
        company.industry = extracted["industry"]
    if extracted.get("country"):
        company.country = extracted["country"]
    if extracted.get("founded_year"):
        company.founded_year = extracted["founded_year"]
    if extracted.get("website"):
        company.website = extracted["website"]
    company.scraped_data_path = scraped.get("saved_path")

    # 5. Add products (skip duplicates by name)
    existing_product_names = {p.name.lower() for p in company.products}
    for prod in extracted.get("products", []):
        if prod["name"].lower() not in existing_product_names:
            company.products.append(
                Product(name=prod["name"], description=prod.get("description"))
            )

    # 6. Add people (skip duplicates by name)
    existing_people_names = {p.name.lower() for p in company.people}
    for person in extracted.get("people", []):
        if person["name"].lower() not in existing_people_names:
            company.people.append(
                Person(
                    name=person["name"],
                    title=person.get("title", "Unknown"),
                    email=person.get("email") or "unknown",
                    linkedin_url=person.get("linkedin_url"),
                    role_type=person.get("role_type"),
                )
            )

    db.commit()
    db.refresh(company)
    return company
