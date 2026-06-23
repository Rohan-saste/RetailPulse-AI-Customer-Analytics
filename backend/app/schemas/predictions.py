from pydantic import BaseModel
from typing import List, Optional


class ChurnPredictionRequest(BaseModel):
    recency: int
    frequency: int
    monetary: float
    avg_revenue: float
    total_items: int
    avg_quantity: float


class ChurnPredictionResponse(BaseModel):
    probability: float
    prediction: int
    risk_level: str  # "Low", "Medium", "High"


class ChurnOverview(BaseModel):
    total_customers: int
    churned_customers: int
    churn_rate: float


class ForecastPoint(BaseModel):
    ds: str
    yhat: float
    yhat_lower: float
    yhat_upper: float


class ForecastSummary(BaseModel):
    projected_total: float
    projected_avg_daily: float
    horizon_days: int


class PipelineStatus(BaseModel):
    job_id: str
    status: str  # "running", "completed", "failed"
    message: str
