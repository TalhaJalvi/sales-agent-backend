"""Pydantic schemas for request/response models."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Product(BaseModel):
    """Product schema."""

    model_config = ConfigDict(strict=True, from_attributes=True)

    id: int
    company_id: int
    name: str
    description: str | None = None
    created_at: datetime


class Person(BaseModel):
    """Person schema."""

    model_config = ConfigDict(strict=True, from_attributes=True)

    id: int
    company_id: int
    name: str
    title: str
    email: str
    linkedin_url: str | None = None
    role_type: str | None = None
    created_at: datetime


class Company(BaseModel):
    """Company schema."""

    model_config = ConfigDict(strict=True, from_attributes=True)

    id: int
    name: str
    website: str | None = None
    description: str | None = None
    industry: str | None = None
    country: str | None = None
    founded_year: int | None = None
    scraped_data_path: str | None = None
    created_at: datetime
    updated_at: datetime
    products: list[Product] = []
    people: list[Person] = []


class Campaign(BaseModel):
    """Campaign schema."""

    model_config = ConfigDict(strict=True, from_attributes=True)

    id: int
    name: str
    description: str | None = None
    company_id: int
    status: str = "pending"
    pitch_content: str | None = None
    notes: str | None = None
    created_at: datetime
    updated_at: datetime
    person_ids: list[int] = []
    product_ids: list[int] = []
    people: list[Person] = []
    products: list[Product] = []
