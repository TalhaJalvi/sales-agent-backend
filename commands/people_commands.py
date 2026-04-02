"""Write operations for people."""

from sqlalchemy.orm import Session

from models import Person


def create_person(
    db: Session,
    company_id: int,
    name: str,
    title: str,
    email: str,
    linkedin_url: str | None = None,
    role_type: str | None = None,
) -> Person:
    person = Person(
        company_id=company_id,
        name=name,
        title=title,
        email=email,
        linkedin_url=linkedin_url,
        role_type=role_type,
    )
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


def update_person(db: Session, person_id: int, **fields) -> Person:
    person = db.get(Person, person_id)
    if person is None:
        raise ValueError(f"Person {person_id} not found")
    for key, value in fields.items():
        setattr(person, key, value)
    db.commit()
    db.refresh(person)
    return person


def delete_person(db: Session, person_id: int) -> None:
    person = db.get(Person, person_id)
    if person is None:
        raise ValueError(f"Person {person_id} not found")
    db.delete(person)
    db.commit()
