"""Read operations for people."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Person


def get_person(db: Session, person_id: int) -> Person | None:
    return db.get(Person, person_id)


def list_people_by_company(db: Session, company_id: int) -> list[Person]:
    return list(
        db.scalars(
            select(Person)
            .where(Person.company_id == company_id)
            .order_by(Person.created_at.desc())
        )
    )


def search_people(db: Session, query: str) -> list[Person]:
    pattern = f"%{query}%"
    return list(
        db.scalars(
            select(Person)
            .where(
                Person.name.ilike(pattern)
                | Person.title.ilike(pattern)
                | Person.email.ilike(pattern)
            )
            .order_by(Person.created_at.desc())
        )
    )
