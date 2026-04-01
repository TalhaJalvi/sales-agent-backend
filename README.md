# Sales Agent Backend

A backend API for managing B2B sales outreach — companies, contacts, products, and campaigns — built with FastAPI and PostgreSQL.

## Tech Stack

- **Framework:** FastAPI + Uvicorn
- **Database:** PostgreSQL (via Supabase)
- **ORM:** SQLAlchemy 2.0 (mapped columns, type-safe relationships)
- **Migrations:** Alembic
- **Validation:** Pydantic v2 (strict mode, ORM integration)
- **Package Manager:** uv

## Architecture

The project follows a **CQRS-inspired** layered architecture:

```
backend/
├── routes/          # API endpoints (FastAPI routers)
├── commands/        # Write operations (create, update, delete)
├── queries/         # Read operations (get, list, search)
├── services/        # Business logic
├── schemas.py       # Pydantic request/response models
├── models.py        # SQLAlchemy ORM models
├── database.py      # DB engine, session, dependency injection
├── dependencies.py  # Shared FastAPI dependencies
├── alembic/         # Database migrations
├── data/scraped/    # Scraped company data storage
└── tests/
    ├── unit/        # Unit tests (commands, queries, services)
    └── integration/ # Integration tests
```

## Data Model

```
Company (1) ──── (*) Product
   |                    |
   |                    * (campaign_products)
   |                    |
   └──── (*) Campaign ──┘
   |                    |
   |                    * (campaign_people)
   |                    |
   └──── (*) Person ────┘
```

- **Company** — target organization with industry, website, and scraped data
- **Person** — contact at a company (title, email, LinkedIn, role type)
- **Product** — product/service offered by a company
- **Campaign** — outreach campaign linking a company to specific people and products

## Getting Started

### Prerequisites

- Python 3.13+
- PostgreSQL
- [uv](https://docs.astral.sh/uv/)

### Setup

```bash
# Clone the repo
git clone https://github.com/<your-username>/sales-agent-backend.git
cd sales-agent-backend

# Install dependencies
uv sync

# Configure environment
cp .env.example .env
# Edit .env with your PostgreSQL connection string

# Run migrations
uv run alembic upgrade head

# Start the server
uv run uvicorn main:app --reload
```

## API Documentation

Once the server is running, interactive docs are available at:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## License

MIT
