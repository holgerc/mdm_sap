"""API v1 router configuration."""
from fastapi import APIRouter
from app.api.v1.endpoints import entities, attributes, catalogs, auth, health

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(entities.router, prefix="/entities", tags=["Entities"])
api_router.include_router(attributes.router, prefix="/attributes", tags=["Attributes"])
api_router.include_router(catalogs.router, prefix="/catalogs", tags=["Catalogs"])
