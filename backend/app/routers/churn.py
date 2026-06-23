from fastapi import APIRouter, Depends, Query
from app.middleware.auth import get_current_user
from app.services.data_service import data_service
from app.services.ml_service import ml_service
from app.schemas.predictions import ChurnPredictionRequest, ChurnPredictionResponse

router = APIRouter(prefix="/churn", tags=["Churn Risk Intelligence"])


@router.get("/overview")
def get_churn_overview(_=Depends(get_current_user)):
    """Get churn overview statistics."""
    result = data_service.get_churn_overview()
    if result is None:
        return {"error": "Churn data not available"}
    return result


@router.post("/predict", response_model=ChurnPredictionResponse)
def predict_churn(
    request: ChurnPredictionRequest,
    _=Depends(get_current_user),
):
    """Run churn prediction on customer features."""
    result = ml_service.predict_churn(
        recency=request.recency,
        frequency=request.frequency,
        monetary=request.monetary,
        avg_revenue=request.avg_revenue,
        total_items=request.total_items,
        avg_quantity=request.avg_quantity,
    )
    if result is None:
        return ChurnPredictionResponse(probability=0.0, prediction=0, risk_level="Unknown")
    return ChurnPredictionResponse(**result)


@router.get("/risk-list")
def get_risk_list(
    n: int = Query(100),
    _=Depends(get_current_user),
):
    """Get top N churned customer profiles sorted by dormancy."""
    return data_service.get_churn_risk_list(n)
