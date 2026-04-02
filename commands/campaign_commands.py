"""Write operations for campaigns."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Campaign, Person, Product


def create_campaign(
    db: Session,
    name: str,
    company_id: int,
    description: str | None = None,
    person_ids: list[int] | None = None,
    product_ids: list[int] | None = None,
) -> Campaign:
    campaign = Campaign(
        name=name,
        company_id=company_id,
        description=description,
    )
    if person_ids:
        people = list(db.scalars(select(Person).where(Person.id.in_(person_ids))))
        campaign.people = people
    if product_ids:
        products = list(db.scalars(select(Product).where(Product.id.in_(product_ids))))
        campaign.products = products
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign


def update_campaign(db: Session, campaign_id: int, **fields) -> Campaign:
    campaign = db.get(Campaign, campaign_id)
    if campaign is None:
        raise ValueError(f"Campaign {campaign_id} not found")

    person_ids = fields.pop("person_ids", None)
    product_ids = fields.pop("product_ids", None)

    for key, value in fields.items():
        setattr(campaign, key, value)

    if person_ids is not None:
        people = list(db.scalars(select(Person).where(Person.id.in_(person_ids))))
        campaign.people = people
    if product_ids is not None:
        products = list(db.scalars(select(Product).where(Product.id.in_(product_ids))))
        campaign.products = products

    db.commit()
    db.refresh(campaign)
    return campaign


def delete_campaign(db: Session, campaign_id: int) -> None:
    campaign = db.get(Campaign, campaign_id)
    if campaign is None:
        raise ValueError(f"Campaign {campaign_id} not found")
    db.delete(campaign)
    db.commit()
