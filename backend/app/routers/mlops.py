from fastapi import APIRouter, Depends
from app.middleware.auth import get_current_user, require_role
from app.services.data_service import data_service
from app.services.pipeline_service import trigger_retrain, get_job_status

router = APIRouter(prefix="/mlops", tags=["MLOps Observability"])


@router.get("/drift-report")
def get_drift_report(_=Depends(get_current_user)):
    """Get the latest data drift analysis report."""
    if data_service.drift_report is None:
        return {"error": "No drift report available. Run drift analysis first."}
    return data_service.drift_report


@router.post("/retrain")
def trigger_pipeline(_=Depends(require_role("admin"))):
    """Trigger the full retrain pipeline (admin only)."""
    result = trigger_retrain()
    return result


@router.get("/retrain/{job_id}")
def check_retrain_status(job_id: str, _=Depends(get_current_user)):
    """Check the status of a retrain pipeline job."""
    return get_job_status(job_id)
