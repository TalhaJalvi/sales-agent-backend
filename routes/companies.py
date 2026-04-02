"""Company routes."""

from fastapi import APIRouter
from pydantic import BaseModel

from commands.company_commands import create_company, delete_company, update_company
from commands.enrichment_commands import enrich_company
from dependencies import DbSession
from queries.company_queries import get_company, list_companies, search_companies
from schemas import Company

router = APIRouter(prefix="/api/companies", tags=["companies"])


class CreateCompanyBody(BaseModel):
    name: str
    description: str
    industry: str
    country: str
    founded_year: int
    website: str | None = None


class UpdateCompanyBody(BaseModel):
    name: str | None = None
    website: str | None = None
    description: str | None = None
    industry: str | None = None
    country: str | None = None
    founded_year: int | None = None


@router.get("/", response_model=list[Company])
def get_companies(db: DbSession, q: str | None = None):
    if q:
        return search_companies(db, q)
    return list_companies(db)


@router.get("/{company_id}", response_model=Company)
def get_company_by_id(db: DbSession, company_id: int):
    return get_company(db, company_id)


@router.post("/", response_model=Company, status_code=201)
def create_company_route(db: DbSession, body: CreateCompanyBody):
    return create_company(
        db,
        name=body.name,
        website=body.website,
        description=body.description,
        industry=body.industry,
        country=body.country,
        founded_year=body.founded_year,
    )


@router.patch("/{company_id}", response_model=Company)
def update_company_route(db: DbSession, company_id: int, body: UpdateCompanyBody):
    fields = body.model_dump(exclude_unset=True)
    return update_company(db, company_id, **fields)


@router.delete("/{company_id}")
def delete_company_route(db: DbSession, company_id: int):
    delete_company(db, company_id)
    return {"detail": "Company deleted"}


@router.post("/{company_id}/enrich", response_model=Company)
def enrich_company_route(db: DbSession, company_id: int):
    return enrich_company(db, company_id)
