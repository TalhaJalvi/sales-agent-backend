"""AI routes — pitch generation and target recommendation."""

import json

from fastapi import APIRouter
from pydantic import BaseModel

from dependencies import DbSession
from queries.company_queries import get_company
from queries.people_queries import get_person, list_people_by_company
from services.ai_service import generate_pitch, recommend_targets

router = APIRouter(prefix="/api/ai", tags=["ai"])


class GeneratePitchBody(BaseModel):
    company_id: int
    person_id: int
    user_product: str


class RecommendTargetsBody(BaseModel):
    company_id: int
    user_product: str


@router.post("/generate-pitch")
def generate_pitch_route(db: DbSession, body: GeneratePitchBody):
    company = get_company(db, body.company_id)
    if company is None:
        raise ValueError(f"Company {body.company_id} not found")

    person = get_person(db, body.person_id)
    if person is None:
        raise ValueError(f"Person {body.person_id} not found")

    company_info = f"Name: {company.name}\nIndustry: {company.industry}\nDescription: {company.description}\nCountry: {company.country}"

    pitch = generate_pitch(
        company_info=company_info,
        person_name=person.name,
        person_title=person.title,
        user_product=body.user_product,
    )
    return {"pitch": pitch}


@router.post("/recommend-targets")
def recommend_targets_route(db: DbSession, body: RecommendTargetsBody):
    company = get_company(db, body.company_id)
    if company is None:
        raise ValueError(f"Company {body.company_id} not found")

    people = list_people_by_company(db, body.company_id)
    if not people:
        return {"targets": [], "message": "No people found for this company"}

    company_info = f"Name: {company.name}\nIndustry: {company.industry}\nDescription: {company.description}\nCountry: {company.country}"
    people_json = json.dumps(
        [{"name": p.name, "title": p.title, "role_type": p.role_type} for p in people]
    )

    targets = recommend_targets(
        company_info=company_info,
        people_json=people_json,
        user_product=body.user_product,
    )
    return {"targets": targets}
