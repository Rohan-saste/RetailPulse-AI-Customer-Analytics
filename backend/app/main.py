# ==============================================================
# RetailPulse Server – FastAPI Application Entry Point
# ==============================================================

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

from app.config import settings
from app.database import create_tables
from app.services.data_service import data_service
from app.services.ml_service import ml_service
from app.utils.logger import logger

# Import all routers
from app.routers import auth, dashboard, eda, analytics, segmentation, forecast, churn, inventory, mlops, reports


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle handler."""
    # ── STARTUP ──────────────────────────────────────────
    logger.info("=" * 60)
    logger.info("  RetailPulse API Server Starting...")
    logger.info("=" * 60)

    # Create database tables
    create_tables()
    logger.info("Database tables created/verified")

    # Load CSV datasets into memory
    data_service.load_all()

    # Load ML models
    ml_service.load_models()

    logger.info("=" * 60)
    logger.info("  RetailPulse API Server Ready!")
    logger.info("=" * 60)

    yield

    # ── SHUTDOWN ─────────────────────────────────────────
    logger.info("RetailPulse API Server shutting down...")


# ── Create FastAPI App ──────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered Customer Analytics & Demand Forecasting API",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS Middleware ─────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request Logging Middleware ──────────────────────────────
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round((time.time() - start) * 1000, 2)
    logger.info(f"{request.method} {request.url.path} → {response.status_code} ({duration}ms)")
    return response


# ── Global Exception Handler ───────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error on {request.method} {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": type(exc).__name__},
    )


# ── Register Routers ───────────────────────────────────────
API_PREFIX = "/api/v1"
app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(dashboard.router, prefix=API_PREFIX)
app.include_router(eda.router, prefix=API_PREFIX)
app.include_router(analytics.router, prefix=API_PREFIX)
app.include_router(segmentation.router, prefix=API_PREFIX)
app.include_router(forecast.router, prefix=API_PREFIX)
app.include_router(churn.router, prefix=API_PREFIX)
app.include_router(inventory.router, prefix=API_PREFIX)
app.include_router(mlops.router, prefix=API_PREFIX)
app.include_router(reports.router, prefix=API_PREFIX)


# ── Health Check ────────────────────────────────────────────
@app.get("/api/v1/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "data_loaded": data_service.df is not None,
        "models_loaded": ml_service.model is not None,
    }
