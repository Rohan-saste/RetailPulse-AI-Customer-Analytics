from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class TreemapItem(BaseModel):
    description: str
    revenue: float


class ScatterPoint(BaseModel):
    quantity: float
    price: float
    revenue: float


class SegmentComposition(BaseModel):
    segment: str
    count: int


class SegmentProfile(BaseModel):
    segment: str
    recency: float
    frequency: float
    monetary: float


class Cluster3DPoint(BaseModel):
    recency: float
    frequency: float
    monetary: float
    segment: str


class InventoryItem(BaseModel):
    description: str
    avg_daily_sales: float
    safety_stock: int
    reorder_point: int
    current_stock: int
    status: str


class InventorySummary(BaseModel):
    total_skus: int
    critical_skus: int
    reorder_skus: int
    healthy_skus: int


class DriftMetric(BaseModel):
    ks_statistic: float
    p_value: float
    drift_detected: bool
    ref_mean: float
    curr_mean: float


class DriftReport(BaseModel):
    status: str
    reference_period: str
    reference_rows: int
    current_period: str
    current_rows: int
    drift_detected: bool
    metrics: Dict[str, DriftMetric]
