"""People routes."""

from fastapi import APIRouter
from pydantic import BaseModel

from commands.people_commands import create_person, delete_person, update_person
from dependencies import DbSession
from queries.people_queries import get_person, list_people_by_company, search_people
from schemas import Person

router = APIRouter(prefix="/api/people", tags=["people"])


class CreatePersonBody(BaseModel):
    company_id: int
    name: str
    title: str
    email: str
    linkedin_url: str | None = None
    role_type: str | None = None


class UpdatePersonBody(BaseModel):
    name: str | None = None
    title: str | None = None
    email: str | None = None
    linkedin_url: str | None = None
    role_type: str | None = None


@router.get("/", response_model=list[Person])
def get_people(db: DbSession, company_id: int | None = None, q: str | None = None):
    if q:
        return search_people(db, q)
    if company_id:
        return list_people_by_company(db, company_id)
    return search_people(db, "")


@router.get("/{person_id}", response_model=Person)
def get_person_by_id(db: DbSession, person_id: int):
    return get_person(db, person_id)


@router.post("/", response_model=Person, status_code=201)
def create_person_route(db: DbSession, body: CreatePersonBody):
    return create_person(
        db,
        company_id=body.company_id,
        name=body.name,
        title=body.title,
        email=body.email,
        linkedin_url=body.linkedin_url,
        role_type=body.role_type,
    )


@router.patch("/{person_id}", response_model=Person)
def update_person_route(db: DbSession, person_id: int, body: UpdatePersonBody):
    fields = body.model_dump(exclude_unset=True)
    return update_person(db, person_id, **fields)


@router.delete("/{person_id}")
def delete_person_route(db: DbSession, person_id: int):
    delete_person(db, person_id)
    return {"detail": "Person deleted"}
