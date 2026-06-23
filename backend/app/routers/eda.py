from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.middleware.auth import get_current_user
from app.services.data_service import data_service

router = APIRouter(prefix="/eda", tags=["Exploratory Data Analysis"])


@router.get("/distributions")
def get_distributions(
    countries: Optional[str] = Query(None),
    years: Optional[str] = Query(None),
    _=Depends(get_current_user),
):
    """Get revenue, price, and quantity distributions (capped at 98th percentile)."""
    c = countries.split(",") if countries else None
    y = [int(x) for x in years.split(",")] if years else None
    filtered = data_service.get_filtered_df(countries=c, years=y)
    return data_service.get_distributions(filtered)


@router.get("/temporal-heatmap")
def get_temporal_heatmap(
    countries: Optional[str] = Query(None),
    years: Optional[str] = Query(None),
    _=Depends(get_current_user),
):
    """Get weekday × hour revenue heatmap data."""
    c = countries.split(",") if countries else None
    y = [int(x) for x in years.split(",")] if years else None
    filtered = data_service.get_filtered_df(countries=c, years=y)
    return data_service.get_temporal_heatmap(filtered)


@router.get("/weekly-revenue")
def get_weekly_revenue(
    countries: Optional[str] = Query(None),
    years: Optional[str] = Query(None),
    _=Depends(get_current_user),
):
    """Get revenue by day of week."""
    c = countries.split(",") if countries else None
    y = [int(x) for x in years.split(",")] if years else None
    filtered = data_service.get_filtered_df(countries=c, years=y)
    return data_service.get_weekly_revenue(filtered)


@router.get("/correlations")
def get_correlations(
    countries: Optional[str] = Query(None),
    years: Optional[str] = Query(None),
    _=Depends(get_current_user),
):
    """Get correlation matrix for Quantity, Price, Revenue."""
    c = countries.split(",") if countries else None
    y = [int(x) for x in years.split(",")] if years else None
    filtered = data_service.get_filtered_df(countries=c, years=y)
    return data_service.get_correlations(filtered)


@router.get("/stats")
def get_stats(
    countries: Optional[str] = Query(None),
    years: Optional[str] = Query(None),
    _=Depends(get_current_user),
):
    """Get descriptive statistics for numerical columns."""
    c = countries.split(",") if countries else None
    y = [int(x) for x in years.split(",")] if years else None
    filtered = data_service.get_filtered_df(countries=c, years=y)
    return data_service.get_stats(filtered)
