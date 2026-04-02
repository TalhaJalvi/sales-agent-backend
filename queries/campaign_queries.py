"""Read operations for campaigns."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Campaign


def get_campaign(db: Session, campaign_id: int) -> Campaign | None:
    return db.get(Campaign, campaign_id)


def list_campaigns(db: Session) -> list[Campaign]:
    return list(
        db.scalars(select(Campaign).order_by(Campaign.created_at.desc()))
    )


def list_campaigns_by_company(db: Session, company_id: int) -> list[Campaign]:
    return list(
        db.scalars(
            select(Campaign)
            .where(Campaign.company_id == company_id)
            .order_by(Campaign.created_at.desc())
        )
    )


def filter_campaigns_by_status(db: Session, status: str) -> list[Campaign]:
    return list(
        db.scalars(
            select(Campaign)
            .where(Campaign.status == status)
            .order_by(Campaign.created_at.desc())
        )
    )
