from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from app.middleware.auth import get_current_user
from app.services.data_service import data_service

router = APIRouter(prefix="/dashboard", tags=["Executive Dashboard"])


@router.get("/filters")
def get_filters(_=Depends(get_current_user)):
    """Get available filter options (countries, years, date range)."""
    return data_service.get_available_filters()


@router.get("/kpis")
def get_kpis(
    countries: Optional[str] = Query(None),
    years: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    _=Depends(get_current_user),
):
    """Get executive KPI metrics with sparkline data."""
    from datetime import date as date_type
    c = countries.split(",") if countries else None
    y = [int(x) for x in years.split(",")] if years else None
    sd = date_type.fromisoformat(start_date) if start_date else None
    ed = date_type.fromisoformat(end_date) if end_date else None
    filtered = data_service.get_filtered_df(countries=c, years=y, start_date=sd, end_date=ed)
    return data_service.get_kpis(filtered)


@router.get("/monthly-revenue")
def get_monthly_revenue(
    countries: Optional[str] = Query(None),
    years: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    _=Depends(get_current_user),
):
    """Get monthly revenue trend data."""
    from datetime import date as date_type
    c = countries.split(",") if countries else None
    y = [int(x) for x in years.split(",")] if years else None
    sd = date_type.fromisoformat(start_date) if start_date else None
    ed = date_type.fromisoformat(end_date) if end_date else None
    filtered = data_service.get_filtered_df(countries=c, years=y, start_date=sd, end_date=ed)
    return data_service.get_monthly_revenue(filtered)


@router.get("/geo-revenue")
def get_geo_revenue(
    countries: Optional[str] = Query(None),
    years: Optional[str] = Query(None),
    _=Depends(get_current_user),
):
    """Get geographic revenue distribution."""
    c = countries.split(",") if countries else None
    y = [int(x) for x in years.split(",")] if years else None
    filtered = data_service.get_filtered_df(countries=c, years=y)
    return data_service.get_geo_revenue(filtered)


@router.get("/top-products")
def get_top_products(
    countries: Optional[str] = Query(None),
    years: Optional[str] = Query(None),
    n: int = Query(10),
    _=Depends(get_current_user),
):
    """Get top N revenue-generating products."""
    c = countries.split(",") if countries else None
    y = [int(x) for x in years.split(",")] if years else None
    filtered = data_service.get_filtered_df(countries=c, years=y)
    return data_service.get_top_products(filtered, n)


@router.get("/top-countries")
def get_top_countries(
    countries: Optional[str] = Query(None),
    years: Optional[str] = Query(None),
    n: int = Query(8),
    _=Depends(get_current_user),
):
    """Get top N countries by revenue."""
    c = countries.split(",") if countries else None
    y = [int(x) for x in years.split(",")] if years else None
    filtered = data_service.get_filtered_df(countries=c, years=y)
    return data_service.get_top_countries(filtered, n)
