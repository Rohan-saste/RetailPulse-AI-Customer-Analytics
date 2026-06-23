from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.middleware.auth import get_current_user
from app.services.data_service import data_service

router = APIRouter(prefix="/analytics", tags=["Sales & Financial Analytics"])


@router.get("/treemap")
def get_treemap(
    countries: Optional[str] = Query(None),
    years: Optional[str] = Query(None),
    n: int = Query(35),
    _=Depends(get_current_user),
):
    """Get product revenue treemap data."""
    c = countries.split(",") if countries else None
    y = [int(x) for x in years.split(",")] if years else None
    filtered = data_service.get_filtered_df(countries=c, years=y)
    return data_service.get_treemap_data(filtered, n)


@router.get("/scatter")
def get_scatter(
    countries: Optional[str] = Query(None),
    years: Optional[str] = Query(None),
    n: int = Query(1500),
    _=Depends(get_current_user),
):
    """Get quantity vs price scatter data (sampled)."""
    c = countries.split(",") if countries else None
    y = [int(x) for x in years.split(",")] if years else None
    filtered = data_service.get_filtered_df(countries=c, years=y)
    return data_service.get_scatter_data(filtered, n)
