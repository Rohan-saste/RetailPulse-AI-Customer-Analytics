# ==============================================================
# RetailPulse Server – Pipeline Service (Retrain Orchestration)
# ==============================================================

import subprocess
import sys
import os
import uuid
from typing import Dict
from app.config import settings
from app.utils.logger import logger


# In-memory job tracking
_jobs: Dict[str, Dict] = {}


def trigger_retrain() -> Dict:
    """Trigger the full retrain pipeline as a background process."""
    job_id = str(uuid.uuid4())[:8]
    _jobs[job_id] = {"status": "running", "message": "Pipeline triggered"}

    logger.info(f"Pipeline retrain triggered (job_id: {job_id})")

    # Locate the pipeline scripts directory
    notebooks_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "..", "RetailPulse", "notebooks"
    )

    if not os.path.exists(notebooks_dir):
        _jobs[job_id] = {"status": "failed", "message": f"Notebooks directory not found: {notebooks_dir}"}
        return _jobs[job_id]

    pipeline_steps = [
        "02_data_cleaning.py",
        "04_05_segmentation.py",
        "06_demand_forecasting.py",
        "07_churn_prediction.py",
        "08_mlops_monitoring.py",
    ]

    for step in pipeline_steps:
        script_path = os.path.join(notebooks_dir, step)
        if not os.path.exists(script_path):
            _jobs[job_id] = {"status": "failed", "message": f"Script not found: {step}"}
            logger.error(f"Pipeline step missing: {script_path}")
            return _jobs[job_id]

        logger.info(f"  Running pipeline step: {step}")
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=notebooks_dir,
            env=env,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            _jobs[job_id] = {
                "status": "failed",
                "message": f"Step {step} failed: {result.stderr[:500]}",
            }
            logger.error(f"  Step {step} failed: {result.stderr[:200]}")
            return _jobs[job_id]

    _jobs[job_id] = {"status": "completed", "message": "All pipeline steps completed successfully"}
    logger.info(f"Pipeline retrain completed (job_id: {job_id})")
    return _jobs[job_id]


def get_job_status(job_id: str) -> Dict:
    """Check the status of a retrain job."""
    return _jobs.get(job_id, {"status": "not_found", "message": "Job ID not found"})
