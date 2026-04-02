"""Campaign routes."""

from fastapi import APIRouter
from pydantic import BaseModel

from commands.campaign_commands import create_campaign, delete_campaign, update_campaign
from dependencies import DbSession
from queries.campaign_queries import (
    filter_campaigns_by_status,
    get_campaign,
    list_campaigns,
    list_campaigns_by_company,
)
from schemas import Campaign

router = APIRouter(prefix="/api/campaigns", tags=["campaigns"])


class CreateCampaignBody(BaseModel):
    name: str
    company_id: int
    description: str | None = None
    person_ids: list[int] | None = None
    product_ids: list[int] | None = None


class UpdateCampaignBody(BaseModel):
    name: str | None = None
    description: str | None = None
    status: str | None = None
    pitch_content: str | None = None
    notes: str | None = None
    person_ids: list[int] | None = None
    product_ids: list[int] | None = None


@router.get("/", response_model=list[Campaign])
def get_campaigns(
    db: DbSession,
    company_id: int | None = None,
    status: str | None = None,
):
    if status:
        return filter_campaigns_by_status(db, status)
    if company_id:
        return list_campaigns_by_company(db, company_id)
    return list_campaigns(db)


@router.get("/{campaign_id}", response_model=Campaign)
def get_campaign_by_id(db: DbSession, campaign_id: int):
    return get_campaign(db, campaign_id)


@router.post("/", response_model=Campaign, status_code=201)
def create_campaign_route(db: DbSession, body: CreateCampaignBody):
    return create_campaign(
        db,
        name=body.name,
        company_id=body.company_id,
        description=body.description,
        person_ids=body.person_ids,
        product_ids=body.product_ids,
    )


@router.patch("/{campaign_id}", response_model=Campaign)
def update_campaign_route(db: DbSession, campaign_id: int, body: UpdateCampaignBody):
    fields = body.model_dump(exclude_unset=True)
    return update_campaign(db, campaign_id, **fields)


@router.delete("/{campaign_id}")
def delete_campaign_route(db: DbSession, campaign_id: int):
    delete_campaign(db, campaign_id)
    return {"detail": "Campaign deleted"}
