import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.data.database import init_db, get_db_session
from backend.data.seed import seed_database
from backend.domain.models import Customer
from backend.api.alerts import router as alerts_router
from backend.api.investigations import router as investigations_router
from backend.api.decisions import router as decisions_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize and seed database if empty
    init_db()
    with get_db_session() as session:
        if session.query(Customer).count() == 0:
            seed_database(session)
    yield


app = FastAPI(
    title="AML Alert Investigation Copilot API",
    description="Agentic Banking AML Copilot with Strict Human-in-the-Loop Governance (Banco Río Sur)",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware for compliance console UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health endpoint
@app.get("/api/v1/health")
def health_check():
    """System health check endpoint."""
    return {
        "status": "HEALTHY",
        "institution": "BANK-RIO-SUR",
        "harness": "ACTIVE",
        "invariants_enforced": True,
    }


# Mount API routers
app.include_router(alerts_router, prefix="/api/v1")
app.include_router(investigations_router, prefix="/api/v1")
app.include_router(decisions_router, prefix="/api/v1")

# Mount Static frontend at the end so it doesn't intercept API calls
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
