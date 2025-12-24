"""Health check endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db
from app.core.config import settings
from app.schemas.common import HealthResponse

router = APIRouter()


@router.get("", response_model=HealthResponse)
async def health_check(db: AsyncSession = Depends(get_db)):
    """Check application health status."""
    # Check database connection
    db_status = "disconnected"
    try:
        await db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "error"

    return HealthResponse(
        status="healthy" if db_status == "connected" else "unhealthy",
        version=settings.APP_VERSION,
        database=db_status,
        redis=None  # TODO: Add Redis health check
    )


@router.get("/ready")
async def readiness_check():
    """Kubernetes readiness probe."""
    return {"ready": True}


@router.get("/live")
async def liveness_check():
    """Kubernetes liveness probe."""
    return {"alive": True}
