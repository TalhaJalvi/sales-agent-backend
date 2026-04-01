"""Read operations for companies."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Company


def get_company(db: Session, company_id: int) -> Company | None:
    return db.get(Company, company_id)


def list_companies(db: Session) -> list[Company]:
    return list(db.scalars(select(Company).order_by(Company.created_at.desc())))


def search_companies(db: Session, query: str) -> list[Company]:
    pattern = f"%{query}%"
    return list(
        db.scalars(
            select(Company)
            .where(
                Company.name.ilike(pattern)
                | Company.industry.ilike(pattern)
                | Company.country.ilike(pattern)
            )
            .order_by(Company.created_at.desc())
        )
    )
