from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.middleware.auth import get_current_user
from app.services.data_service import data_service

router = APIRouter(prefix="/inventory", tags=["Inventory Health"])


@router.get("/summary")
def get_inventory_summary(_=Depends(get_current_user)):
    """Get inventory health summary (total, critical, reorder, healthy SKU counts)."""
    inv = data_service.calculate_inventory_metrics()
    if inv.empty:
        return {"error": "Transaction data not available for inventory calculation"}
    return data_service.get_inventory_summary(inv)


@router.get("/fast-movers")
def get_fast_movers(n: int = Query(10), _=Depends(get_current_user)):
    """Get top N fast-moving products by daily demand rate."""
    inv = data_service.calculate_inventory_metrics()
    fast = inv.sort_values("avg_daily_sales", ascending=False).head(n)
    return data_service.get_inventory_items(fast)


@router.get("/slow-movers")
def get_slow_movers(n: int = Query(10), _=Depends(get_current_user)):
    """Get top N slow-moving products."""
    inv = data_service.calculate_inventory_metrics()
    slow = inv[inv["total_sold"] > 10].sort_values("avg_daily_sales", ascending=True).head(n)
    return data_service.get_inventory_items(slow)


@router.get("/ledger")
def get_inventory_ledger(
    status_filter: Optional[str] = Query(None),
    _=Depends(get_current_user),
):
    """Get full inventory reorder ledger, optionally filtered by status."""
    inv = data_service.calculate_inventory_metrics()
    return data_service.get_inventory_items(inv, status_filter)
