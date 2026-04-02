"""Write operations for companies."""

from sqlalchemy.orm import Session

from models import Company


def create_company(
    db: Session,
    name: str,
    description: str,
    industry: str,
    country: str,
    founded_year: int,
    website: str | None = None,
) -> Company:
    company = Company(
        name=name,
        website=website,
        description=description,
        industry=industry,
        country=country,
        founded_year=founded_year,
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def update_company(db: Session, company_id: int, **fields) -> Company:
    company = db.get(Company, company_id)
    if company is None:
        raise ValueError(f"Company {company_id} not found")
    for key, value in fields.items():
        setattr(company, key, value)
    db.commit()
    db.refresh(company)
    return company


def delete_company(db: Session, company_id: int) -> None:
    company = db.get(Company, company_id)
    if company is None:
        raise ValueError(f"Company {company_id} not found")
    db.delete(company)
    db.commit()
