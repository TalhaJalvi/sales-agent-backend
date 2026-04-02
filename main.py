"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.ai import router as ai_router
from routes.campaigns import router as campaigns_router
from routes.companies import router as companies_router
from routes.discover import router as discover_router
from routes.people import router as people_router

app = FastAPI(title="Sales Agent API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(companies_router)
app.include_router(people_router)
app.include_router(campaigns_router)
app.include_router(ai_router)
app.include_router(discover_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
