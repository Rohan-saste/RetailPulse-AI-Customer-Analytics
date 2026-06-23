from fastapi import APIRouter, Depends, Query
from typing import Optional, List
from app.middleware.auth import get_current_user
from app.services.data_service import data_service

router = APIRouter(prefix="/segmentation", tags=["Customer Segmentation"])


@router.get("/composition")
def get_composition(
    segments: Optional[str] = Query(None),
    _=Depends(get_current_user),
):
    """Get segment composition (count per segment)."""
    s = segments.split(",") if segments else None
    segs = data_service.get_filtered_segments(s)
    if segs is None:
        return {"error": "Segment data not available"}
    return data_service.get_segment_composition(segs)


@router.get("/profile")
def get_profile(
    segments: Optional[str] = Query(None),
    _=Depends(get_current_user),
):
    """Get segment centroid profile metrics (avg RFM per segment)."""
    s = segments.split(",") if segments else None
    segs = data_service.get_filtered_segments(s)
    if segs is None:
        return {"error": "Segment data not available"}
    return data_service.get_segment_profile(segs)


@router.get("/clusters-3d")
def get_clusters_3d(
    segments: Optional[str] = Query(None),
    n: int = Query(1800),
    _=Depends(get_current_user),
):
    """Get 3D scatter data for RFM cluster visualization."""
    s = segments.split(",") if segments else None
    segs = data_service.get_filtered_segments(s)
    if segs is None:
        return {"error": "Segment data not available"}
    return data_service.get_cluster_3d(segs, n)
