from fastapi import APIRouter, Depends, Query
from app.middleware.auth import get_current_user
from app.services.data_service import data_service

router = APIRouter(prefix="/forecast", tags=["Demand Forecasting"])


@router.get("/data")
def get_forecast_data(
    horizon_days: int = Query(90, ge=30, le=90),
    _=Depends(get_current_user),
):
    """Get forecast trajectory data with actual sales overlay."""
    return data_service.get_forecast_data(horizon_days)
