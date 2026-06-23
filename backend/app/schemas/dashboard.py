from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import date


class FilterParams(BaseModel):
    countries: Optional[List[str]] = None
    years: Optional[List[int]] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    segments: Optional[List[str]] = None


class KPIResponse(BaseModel):
    total_revenue: float
    total_orders: int
    total_customers: int
    avg_order_value: float
    total_products: int
    num_countries: int
    sparklines: Dict[str, List[float]]


class MonthlyRevenuePoint(BaseModel):
    period: str
    revenue: float


class GeoRevenuePoint(BaseModel):
    country: str
    revenue: float


class ProductRevenuePoint(BaseModel):
    description: str
    revenue: float


class DistributionData(BaseModel):
    values: List[float]
    label: str


class HeatmapData(BaseModel):
    weekdays: List[str]
    hours: List[int]
    values: List[List[Optional[float]]]


class CorrelationData(BaseModel):
    labels: List[str]
    matrix: List[List[float]]


class StatsRow(BaseModel):
    metric: str
    quantity: float
    price: float
    revenue: float
